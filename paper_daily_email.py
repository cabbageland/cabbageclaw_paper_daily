#!/usr/bin/env python3
import argparse
import csv
import hashlib
import html
import json
import re
import smtplib
import ssl
import subprocess
import time
import urllib.request
from datetime import date, datetime
from email.message import EmailMessage
from email.utils import getaddresses
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIGEST_DIR = ROOT / "daily_papers"
NOTES_DIR = ROOT / "paper_notes"
RECIPIENTS_CSV = ROOT / "recipients.csv"
INTERNAL_TEST_RECIPIENTS_CSV = ROOT / "recipients-internal-test.csv"
CONFIG_PATH = Path.home() / ".config" / "himalaya" / "config.toml"
SITE_BASE = "https://cabbageland.github.io/cabbageclaw-paper-daily-web"
CONTENT_JSON_URL = f"{SITE_BASE}/data/content.json"
STATE_DIR = ROOT / ".state"
SEND_STATE_PATH = STATE_DIR / "email_send_state.json"
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
REDACTED_EMAIL = "[redacted-email]"
SEND_STATE_VERSION = 2
GITHUB_SOURCE_BASE = "https://github.com/cabbageland/cabbageclaw_paper_daily/blob/main"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="Digest date in YYYY-MM-DD format. Defaults to today.")
    p.add_argument("--to", action="append", default=[], help="Optional extra recipient. Repeatable.")
    p.add_argument("--dry-run", action="store_true", help="Render output but do not send.")
    p.add_argument("--preview-path", help="Write rendered redacted preview to this path.")
    p.add_argument(
        "--internal-test",
        action="store_true",
        help="Send only to recipients-internal-test.csv for debugging or maintenance.",
    )
    return p.parse_args()


def pick_date(date_str: str | None) -> str:
    if date_str:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    return date.today().isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_markdown_emphasis(text: str) -> str:
    return text.replace("**", "").replace("`", "").strip()


def extract_markdown_section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n+(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.M | re.S)
    if not match:
        return ""
    paragraphs = [line.strip() for line in match.group(1).splitlines() if line.strip()]
    return strip_markdown_emphasis(" ".join(paragraphs))


def normalize_repo_path(path: str) -> str:
    cleaned = path.strip()
    cleaned = re.sub(r"^\.\./", "", cleaned)
    return cleaned


def normalize_email(email_address: str) -> str:
    return email_address.strip().lower()


def redact_email_text(text: str) -> str:
    return EMAIL_RE.sub(REDACTED_EMAIL, text)


def recipient_fingerprint(email_address: str) -> str:
    salted = f"paper-daily-recipient:{normalize_email(email_address)}"
    return hashlib.sha256(salted.encode("utf-8")).hexdigest()[:16]


def assert_no_email_tokens(label: str, text: str):
    if EMAIL_RE.search(text):
        raise ValueError(f"{label} contains an unredacted email address")


def assert_no_known_recipient_addresses(label: str, text: str, recipients: list[str]):
    lowered = text.lower()
    leaked = [r for r in recipients if normalize_email(r) in lowered]
    if leaked:
        raise ValueError(f"{label} contains {len(leaked)} recipient email address(es)")


def read_recipients(extra: list[str], internal_test: bool = False) -> list[str]:
    if internal_test and extra:
        raise ValueError("Internal test mode only allows recipients-internal-test.csv recipients")
    recipients = []
    recipients_path = INTERNAL_TEST_RECIPIENTS_CSV if internal_test else RECIPIENTS_CSV
    if recipients_path.exists():
        with recipients_path.open(newline="", encoding="utf-8") as f:
            for row in csv.reader(f):
                if not row:
                    continue
                email = row[0].strip()
                if email and not email.startswith("#"):
                    recipients.append(email)
    recipients.extend(extra)
    deduped = []
    seen = set()
    for recipient in recipients:
        key = normalize_email(recipient)
        if key not in seen:
            seen.add(key)
            deduped.append(recipient)
    if not deduped:
        raise ValueError("No recipients found. Populate recipients.csv or pass --to.")
    return deduped


def header_addresses(msg: EmailMessage, header: str) -> list[str]:
    return [normalize_email(addr) for _, addr in getaddresses(msg.get_all(header, [])) if addr]


def validate_recipient_privacy(messages: list[EmailMessage], recipients: list[str]):
    errors = []
    expected_recipients = [normalize_email(r) for r in recipients]
    if len(messages) != len(expected_recipients):
        errors.append(f"Expected {len(expected_recipients)} message(s), built {len(messages)}")

    for idx, msg in enumerate(messages):
        expected = expected_recipients[idx] if idx < len(expected_recipients) else None
        to_addrs = header_addresses(msg, "To")
        cc_addrs = header_addresses(msg, "Cc")
        bcc_addrs = header_addresses(msg, "Bcc")
        if expected and to_addrs != [expected]:
            errors.append(f"Message {idx + 1} must have exactly one To recipient")
        if cc_addrs:
            errors.append(f"Message {idx + 1} has Cc recipient(s)")
        if bcc_addrs:
            errors.append(f"Message {idx + 1} has Bcc recipient(s)")

        plain_part = msg.get_body(preferencelist=("plain",))
        html_part = msg.get_body(preferencelist=("html",))
        plain = plain_part.get_content() if plain_part else ""
        html_body = html_part.get_content() if html_part else ""
        assert_no_known_recipient_addresses(f"Message {idx + 1} body", plain + "\n" + html_body, recipients)

    if errors:
        raise ValueError("Recipient privacy gate failed: " + "; ".join(errors))


def parse_digest(path: Path) -> dict:
    text = read_text(path)
    lines = text.splitlines()
    if not lines:
        raise ValueError(f"Digest is empty: {path}")
    head = lines[0].strip()
    match = re.match(r"^# Daily Paper Digest - (\d{4}-\d{2}-\d{2})$", head)
    if not match:
        raise ValueError(f"Unexpected digest title line: {head}")
    digest_date = match.group(1)
    result = {
        "date": digest_date,
        "title": f"Paper Daily, {digest_date}, Reporter: cabbageclaw",
        "theme": "",
        "overview": "",
        "takeaway": "",
        "most_relevant": "",
        "ranked_titles": [],
        "ranked_why": {},
        "detail_note_paths": [],
        "digest_path": f"daily_papers/{digest_date}.md",
    }

    current = None
    blocks: dict[str, list[str]] = {}
    for line in lines[1:]:
        if line.startswith("## "):
            current = line[3:].strip()
            blocks[current] = []
        elif current is not None:
            blocks[current].append(line)

    result["theme"] = strip_markdown_emphasis(
        " ".join(line.strip() for line in blocks.get("Theme", []) if line.strip())
    )
    result["overview"] = "\n".join(blocks.get("Short overview", [])).strip()
    result["takeaway"] = "\n".join(blocks.get("One-paragraph takeaway", [])).strip()
    result["most_relevant"] = "\n".join(blocks.get("Most relevant to cabbageland", [])).strip()

    current_title = None
    for line in blocks.get("Ranked papers", []):
        title_match = re.match(r"### \d+\.\s+\*\*(.+?)\*\*", line.strip())
        if title_match:
            current_title = strip_markdown_emphasis(title_match.group(1).strip())
            result["ranked_titles"].append(current_title)
            continue
        why_match = re.match(r"Why it matters:\s*(.+)", line.strip())
        if current_title and why_match:
            result["ranked_why"][current_title] = strip_markdown_emphasis(why_match.group(1).strip())

    for line in blocks.get("Detailed notes", []):
        link_match = re.match(r"- \[(.+?)\]\((.+?)\)", line.strip())
        if link_match:
            result["detail_note_paths"].append(normalize_repo_path(link_match.group(2)))

    return result


def read_note_metadata(path: str) -> tuple[str | None, str | None, str | None]:
    note_path = ROOT / path
    if not note_path.exists():
        return None, None, None
    text = read_text(note_path)
    title = None
    paper_url = None
    for line in text.splitlines()[:20]:
        if line.startswith("# "):
            title = line[2:].strip()
        if line.startswith("* Link: "):
            paper_url = line.split(": ", 1)[1].strip()
    return title, paper_url, extract_markdown_section(text, "One-paragraph overview")


def build_note_index(digest: dict) -> dict[str, str]:
    mapping = {}
    for note_path in digest["detail_note_paths"]:
        title, _, _ = read_note_metadata(note_path)
        if title:
            mapping[title] = note_path
    return mapping


def public_app_route(path: str) -> str:
    return f"{SITE_BASE}/#/{path}"


def github_source_url(path: str) -> str:
    return f"{GITHUB_SOURCE_BASE}/{path}"


def build_items(digest: dict) -> list[dict]:
    note_index = build_note_index(digest)
    items = []
    for title in digest["ranked_titles"]:
        note_path = note_index.get(title)
        if not note_path:
            continue
        note_title, paper_url, note_overview = read_note_metadata(note_path)
        if not paper_url:
            raise ValueError(f"Missing paper link in note: {note_path}")
        if not note_overview:
            raise ValueError(
                f"Missing email body source for ranked paper: {note_path} lacks One-paragraph overview"
            )
        items.append(
            {
                "title": title,
                "paper_url": paper_url,
                "paper_label": note_title or title,
                "notes_path": note_path,
                "notes_url": public_app_route(note_path),
                "source_url": github_source_url(note_path),
                "body": note_overview,
                "why": digest["ranked_why"].get(title, ""),
            }
        )
    if not items:
        raise ValueError("No ranked papers with preserved note links were available for email rendering")
    return items


def validate_digest_structure(digest: dict, items: list[dict]):
    errors = []
    if len(digest["ranked_titles"]) != 5:
        errors.append(f"Expected exactly 5 ranked papers, found {len(digest['ranked_titles'])}")
    if len(items) < 3:
        errors.append(f"Expected at least 3 ranked papers with preserved notes, found {len(items)}")
    if len(items) > 5:
        errors.append(f"Expected at most 5 ranked papers in email, found {len(items)}")
    if not digest["theme"]:
        errors.append("Missing theme")
    if not digest["takeaway"]:
        errors.append("Missing one-paragraph takeaway")
    if not digest["overview"]:
        errors.append("Missing short overview")
    for idx, item in enumerate(items, start=1):
        if not item["paper_url"].startswith("http"):
            errors.append(f"Item {idx} missing valid paper URL")
        if not item["why"]:
            errors.append(f"Item {idx} missing Why it matters")
        if len(item["body"]) < 120:
            errors.append(f"Item {idx} body looks too short")
    if errors:
        raise ValueError("Email QC failed: " + "; ".join(errors))


def validate_rendered_message(
    msg: EmailMessage,
    recipients: list[str],
    internal_test: bool = False,
    expected_item_count: int = 5,
):
    errors = []
    plain_part = msg.get_body(preferencelist=("plain",))
    html_part = msg.get_body(preferencelist=("html",))
    plain = plain_part.get_content() if plain_part else ""
    html_body = html_part.get_content() if html_part else ""

    if not recipients:
        errors.append("Recipient list is empty")
    if "**" in plain or "**" in html_body:
        errors.append("Raw markdown emphasis leaked into rendered email")
    for token in ["Paper:", "Notes:", "Bottom line:"]:
        if token not in plain:
            errors.append(f"Missing plain-text token: {token}")
    if "<a href=" not in html_body:
        errors.append("HTML body has no hyperlinks")
    expected_links = max(1 + expected_item_count * 2, 7)
    if html_body.count("<a href=") < expected_links:
        errors.append(f"HTML body has fewer hyperlinks than expected for {expected_item_count} items")
    if "Content-Type: multipart/alternative" not in msg.as_string().split("\n\n", 1)[0]:
        errors.append("Message is not multipart/alternative")
    if internal_test:
        allowed = {normalize_email(r) for r in read_recipients([], internal_test=True)}
        if any(normalize_email(r) not in allowed for r in recipients):
            errors.append("Internal test mode recipient is not in recipients-internal-test.csv")
    if errors:
        raise ValueError("Rendered email QC failed: " + "; ".join(errors))


def verify_publish_state_before_send(digest: dict, items: list[dict]):
    errors = []
    try:
        with urllib.request.urlopen(f"{SITE_BASE}/", timeout=15) as response:
            body = response.read(4096).decode("utf-8", errors="ignore")
            if getattr(response, "status", 200) >= 400:
                errors.append(f"{SITE_BASE}/ returned HTTP {response.status}")
            elif "Failed to load dashboard" in body:
                errors.append(f"{SITE_BASE}/ loaded dashboard error page")
    except Exception as exc:
        errors.append(f"{SITE_BASE}/ failed: {exc}")

    try:
        cb = int(time.time())
        with urllib.request.urlopen(f"{CONTENT_JSON_URL}?cb={cb}", timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        markdown = data.get("markdown", {})
        required_paths = [digest["digest_path"], *[item["notes_path"] for item in items]]
        missing = [path for path in required_paths if path not in markdown]
        if missing:
            errors.append(f"live content.json missing markdown entries: {missing}")
    except Exception as exc:
        errors.append(f"{CONTENT_JSON_URL} failed: {exc}")

    if errors:
        raise ValueError("Pre-send publish verification failed: " + "; ".join(errors))


def load_send_state() -> dict:
    if not SEND_STATE_PATH.exists():
        return {}
    try:
        return scrub_send_state(json.loads(read_text(SEND_STATE_PATH)))
    except Exception:
        return {}


def scrub_send_state(state: dict) -> dict:
    if not isinstance(state, dict):
        return {}
    for mode_data in state.values():
        if not isinstance(mode_data, dict):
            continue
        for sent in mode_data.values():
            if not isinstance(sent, dict):
                continue
            raw_recipients = sent.pop("recipients", None)
            if raw_recipients is not None:
                recipients = [str(r) for r in raw_recipients if str(r).strip()]
                sent["recipient_count"] = len(recipients)
                sent["recipient_fingerprints"] = [recipient_fingerprint(r) for r in recipients]
            sent.setdefault("recipient_count", 0)
            sent.setdefault("recipient_fingerprints", [])
            sent["state_version"] = SEND_STATE_VERSION
    return state


def save_send_state(state: dict):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    sanitized = scrub_send_state(state)
    serialized = json.dumps(sanitized, indent=2, sort_keys=True) + "\n"
    assert_no_email_tokens("Send state", serialized)
    SEND_STATE_PATH.write_text(serialized, encoding="utf-8")


def send_mode_key(internal_test: bool) -> str:
    return "internal_test" if internal_test else "production"


def assert_not_already_sent(digest_date: str, recipients: list[str], internal_test: bool = False):
    state = load_send_state()
    mode = send_mode_key(internal_test)
    sent = state.get(mode, {}).get(digest_date)
    if sent:
        prior_count = sent.get("recipient_count", 0)
        raise ValueError(
            f"Refusing duplicate send for {digest_date} in {mode} mode. "
            f"Already sent at {sent.get('sent_at')} to {prior_count} recipient(s)."
        )


def record_send(digest_date: str, recipients: list[str], internal_test: bool = False):
    state = load_send_state()
    mode = send_mode_key(internal_test)
    bucket = state.setdefault(mode, {})
    bucket[digest_date] = {
        "sent_at": datetime.now().isoformat(timespec="seconds"),
        "recipient_count": len(recipients),
        "recipient_fingerprints": [recipient_fingerprint(r) for r in recipients],
        "state_version": SEND_STATE_VERSION,
    }
    save_send_state(state)


def smtp_settings() -> tuple[str, int, str, str]:
    text = read_text(CONFIG_PATH)
    host = re.search(r'message\.send\.backend\.host = "([^"]+)"', text)
    port = re.search(r'message\.send\.backend\.port = (\d+)', text)
    login = re.search(r'message\.send\.backend\.login = "([^"]+)"', text)
    cmd = re.search(r'message\.send\.backend\.auth\.cmd = "([^"]+)"', text)
    if not all([host, port, login, cmd]):
        raise ValueError("Could not parse SMTP settings from Himalaya config")
    password = subprocess.check_output(cmd.group(1), shell=True, text=True).strip()
    return host.group(1), int(port.group(1)), login.group(1), password


def human_date(iso_date: str) -> str:
    parsed = datetime.strptime(iso_date, "%Y-%m-%d")
    return parsed.strftime("%B %-d, %Y")


def render_plain(digest: dict, items: list[dict]) -> str:
    digest_url = public_app_route(digest["digest_path"])
    lines = [
        "Hello!",
        "",
        f"Welcome to the {human_date(digest['date'])} Paper Daily at Cabbageland: {digest_url}",
        "",
        f"Theme: {digest['theme']}",
        "",
    ]
    if digest["most_relevant"]:
        lines.extend([strip_markdown_emphasis(digest["most_relevant"]), ""])
    for item in items:
        lines.extend(
            [
                item["title"],
                f"Paper: {item['paper_url']}",
                f"Notes: {item['notes_url']}",
                item["body"],
                f"Why it matters: {item['why']}",
                "",
            ]
        )
    lines.extend(
        [
            f"Bottom line: {digest['takeaway']}",
            "",
            "Yours,",
            "cabbageclaw 🥬🐾",
        ]
    )
    return "\n".join(lines)


def render_html(digest: dict, items: list[dict]) -> str:
    digest_url = public_app_route(digest["digest_path"])
    parts = [
        "<html><body>",
        "<p>Hello!</p>",
        f"<p>Welcome to the <a href=\"{html.escape(digest_url)}\">{html.escape(human_date(digest['date']))} Paper Daily</a> at Cabbageland.</p>",
        f"<p><strong>Theme:</strong> {html.escape(digest['theme'])}</p>",
    ]
    if digest["most_relevant"]:
        parts.append(f"<p>{html.escape(strip_markdown_emphasis(digest['most_relevant']))}</p>")
    for item in items:
        parts.extend(
            [
                f"<p><strong>{html.escape(item['title'])}</strong></p>",
                (
                    "<p><strong>Paper:</strong> "
                    f"<a href=\"{html.escape(item['paper_url'])}\">{html.escape(item['paper_label'])}</a><br>"
                    f"<strong>Notes:</strong> <a href=\"{html.escape(item['notes_url'])}\">Cabbageland notes</a></p>"
                ),
                f"<p>{html.escape(item['body'])}</p>",
                f"<p><strong>Why it matters:</strong> {html.escape(item['why'])}</p>",
            ]
        )
    parts.extend(
        [
            f"<p><strong>Bottom line:</strong> {html.escape(digest['takeaway'])}</p>",
            "<p><strong>Yours,<br>cabbageclaw 🥬🐾</strong></p>",
            "</body></html>",
        ]
    )
    return "".join(parts)


def build_message(digest: dict, items: list[dict], recipient: str) -> EmailMessage:
    msg = EmailMessage()
    _, _, login, _ = smtp_settings()
    msg["Subject"] = digest["title"]
    msg["From"] = login
    msg["To"] = recipient
    msg.set_content(render_plain(digest, items))
    msg.add_alternative(render_html(digest, items), subtype="html")
    return msg


def send_messages(messages: list[EmailMessage]):
    host, port, login, password = smtp_settings()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(login, password)
        for msg in messages:
            server.send_message(msg)


def serialized_redacted_messages(messages: list[EmailMessage]) -> str:
    serialized = "\n\n".join(redact_email_text(msg.as_string()) for msg in messages)
    assert_no_email_tokens("Redacted message preview", serialized)
    return serialized


def main():
    args = parse_args()
    digest_date = pick_date(args.date)
    digest_path = DIGEST_DIR / f"{digest_date}.md"
    if not digest_path.exists():
        raise SystemExit(f"Digest not found: {digest_path}")
    digest = parse_digest(digest_path)
    items = build_items(digest)
    validate_digest_structure(digest, items)
    recipients = read_recipients(args.to, internal_test=args.internal_test)
    messages = [build_message(digest, items, recipient) for recipient in recipients]
    for msg in messages:
        validate_rendered_message(
            msg,
            [msg["To"]],
            internal_test=args.internal_test,
            expected_item_count=len(items),
        )
    validate_recipient_privacy(messages, recipients)
    verify_publish_state_before_send(digest, items)
    redacted_preview = None
    if args.preview_path:
        redacted_preview = serialized_redacted_messages(messages)
        Path(args.preview_path).write_text(redacted_preview, encoding="utf-8")
    if args.dry_run or args.preview_path:
        if args.dry_run:
            if redacted_preview is None:
                redacted_preview = serialized_redacted_messages(messages)
            print(redacted_preview)
        else:
            print(f"PREVIEW_WRITTEN {args.preview_path}")
        return
    assert_not_already_sent(digest["date"], recipients, internal_test=args.internal_test)
    send_messages(messages)
    record_send(digest["date"], recipients, internal_test=args.internal_test)
    print(f"SENT {digest['date']} to {len(recipients)} recipient(s) individually")


if __name__ == "__main__":
    main()
