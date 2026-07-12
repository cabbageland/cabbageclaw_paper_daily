#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT.parent / "cabbageclaw-paper-daily-web"
MANIFEST = ROOT / "audio_manifest.json"
CONTENT = WEB / "data" / "content.json"
DAILY_DIR = ROOT / "daily_papers"
DEFAULT_BASE_URL = "https://cabbageland.github.io/cabbageclaw-paper-daily-web"
LINK_RE = re.compile(r"\((?:\.\./)?((?:paper_notes|related_work)/[^)#?]+\.md)\)")


@dataclass(frozen=True)
class ExpectedItem:
    key: str
    audio_required: bool


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def newest_digest_key() -> str:
    digests = sorted(p.stem for p in DAILY_DIR.glob("*.md") if p.name != ".gitkeep")
    if not digests:
        fail("no daily digests found")
    return f"daily_papers/{digests[-1]}.md"


def digest_key_for_date(date_str: str | None) -> str:
    if not date_str:
        return newest_digest_key()
    path = DAILY_DIR / f"{date_str}.md"
    if not path.exists():
        fail(f"missing digest for date {date_str}: {path}")
    return f"daily_papers/{path.name}"


def linked_keys_for_digest(digest_key: str) -> list[str]:
    digest_path = ROOT / digest_key
    text = digest_path.read_text(encoding="utf-8")
    return sorted(set(LINK_RE.findall(text)))


def expected_items(digest_key: str) -> list[ExpectedItem]:
    items = [ExpectedItem(digest_key, audio_required=True)]
    for key in linked_keys_for_digest(digest_key):
        items.append(ExpectedItem(key, audio_required=key.startswith("paper_notes/")))
    return items


def verify_local_item(item: ExpectedItem, manifest: dict, content: dict) -> tuple[str, str | None]:
    source_path = ROOT / item.key
    if not source_path.exists():
        fail(f"missing source markdown file: {source_path}")

    markdown = content.get("markdown", {})
    if item.key not in markdown:
        fail(f"{item.key} missing from web data/content.json markdown section")

    manifest_item = manifest.get("items", {}).get(item.key)
    content_audio = content.get("audio", {}).get(item.key)

    if item.audio_required:
        if not manifest_item:
            fail(f"{item.key} missing from audio_manifest.json")
        if not content_audio:
            fail(f"{item.key} missing from web data/content.json audio section")

        audio_path = WEB / manifest_item["audioPath"]
        if not audio_path.exists():
            fail(f"missing audio file: {audio_path}")
        if audio_path.stat().st_size <= 0:
            fail(f"empty audio file: {audio_path}")
        return source_path.as_posix(), audio_path.as_posix()

    return source_path.as_posix(), None


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read())


def head_ok(url: str) -> tuple[int, str | None, str | None]:
    request = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(request, timeout=30) as response:
        return (
            response.status,
            response.headers.get("Content-Length"),
            response.headers.get("Content-Type"),
        )


def verify_live(
    items: list[ExpectedItem],
    manifest: dict,
    digest_key: str,
    base_url: str,
    timeout: int,
    interval: int,
) -> None:
    expected_date = Path(digest_key).stem
    target_is_newest = digest_key == newest_digest_key()
    deadline = time.time() + timeout
    content_url = f"{base_url}/data/content.json?cb={int(time.time())}"
    latest_seen = None

    attempt = 0
    while True:
        attempt += 1
        data = fetch_json(content_url)
        latest_seen = data["digests"][0]["date"] if data.get("digests") else None

        missing_markdown = [item.key for item in items if item.key not in data.get("markdown", {})]
        missing_audio = [
            item.key
            for item in items
            if item.audio_required and item.key not in data.get("audio", {})
        ]
        newest_ok = (not target_is_newest) or latest_seen == expected_date

        print(
            f"attempt {attempt} newest {latest_seen} "
            f"missing_markdown {len(missing_markdown)} missing_audio {len(missing_audio)}"
        )

        if newest_ok and not missing_markdown and not missing_audio:
            break
        if time.time() + interval > deadline:
            fail(
                "live content did not reach expected state before timeout "
                f"(newest={latest_seen}, missing_markdown={missing_markdown}, missing_audio={missing_audio})"
            )
        time.sleep(interval)

    for item in items:
        if not item.audio_required:
            continue
        manifest_item = manifest["items"][item.key]
        audio_path = manifest_item["audioPath"]
        status, length, content_type = head_ok(f"{base_url}/{audio_path}?cb={int(time.time())}")
        print(f"{audio_path} {status} {length} {content_type}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="digest date in YYYY-MM-DD; defaults to newest digest")
    parser.add_argument("--live", action="store_true", help="verify live GitHub Pages state too")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--interval", type=int, default=5)
    args = parser.parse_args(argv)

    digest_key = digest_key_for_date(args.date)
    manifest = load_json(MANIFEST)
    content = load_json(CONTENT)
    items = expected_items(digest_key)

    print(f"Checking {digest_key}")
    for item in items:
        source_path, audio_path = verify_local_item(item, manifest, content)
        print(f"  markdown -> {source_path}")
        if audio_path:
            print(f"  audio -> {audio_path}")

    if args.live:
        verify_live(
            items=items,
            manifest=manifest,
            digest_key=digest_key,
            base_url=args.base_url,
            timeout=args.timeout,
            interval=args.interval,
        )

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
