#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT.parent / "cabbageclaw-paper-daily-web"
CONTENT = WEB / "data" / "content.json"
MANIFEST = ROOT / "audio_manifest.json"
DAILY_DIR = ROOT / "daily_papers"
DEFAULT_BASE_URL = "https://cabbageland.github.io/cabbageclaw-paper-daily-web"


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def newest_digest_key() -> str:
    digests = sorted(p.stem for p in DAILY_DIR.glob("*.md") if p.name != ".gitkeep")
    if not digests:
        fail("no daily digests found")
    return f"daily_papers/{digests[-1]}.md"


def load_expected() -> tuple[str, str, str]:
    key = newest_digest_key()
    if not CONTENT.exists():
        fail(f"missing local web content snapshot: {CONTENT}")
    if not MANIFEST.exists():
        fail(f"missing manifest: {MANIFEST}")

    content = json.loads(CONTENT.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    audio_item = manifest.get("items", {}).get(key)
    if not audio_item:
        fail(f"{key} missing from audio_manifest.json")

    date = Path(key).stem
    audio_path = audio_item.get("audioPath")
    if not audio_path:
        fail(f"{key} missing audioPath in audio_manifest.json")

    if key not in content.get("markdown", {}):
        fail(f"{key} missing from local web markdown section")
    if key not in content.get("audio", {}):
        fail(f"{key} missing from local web audio section")

    return key, date, audio_path


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read())


def head_ok(url: str) -> tuple[int, str | None, str | None]:
    request = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.status, response.headers.get("Content-Length"), response.headers.get("Content-Type")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--interval", type=int, default=5)
    args = parser.parse_args()

    key, expected_date, audio_path = load_expected()
    deadline = time.time() + args.timeout
    cache_buster = str(int(time.time()))
    content_url = f"{args.base_url}/data/content.json?cb={cache_buster}"

    attempt = 0
    while True:
        attempt += 1
        data = fetch_json(content_url)
        newest = data["digests"][0]["date"] if data.get("digests") else None
        has_markdown = key in data.get("markdown", {})
        has_audio = key in data.get("audio", {})
        print(
            f"attempt {attempt} newest {newest} "
            f"has_markdown {has_markdown} has_audio {has_audio}"
        )
        if newest == expected_date and has_markdown and has_audio:
            break
        if time.time() + args.interval > deadline:
            fail("live content did not update before timeout")
        time.sleep(args.interval)

    status, length, content_type = head_ok(f"{args.base_url}/{audio_path}?cb={cache_buster}")
    print(f"{audio_path} {status} {length} {content_type}")


if __name__ == "__main__":
    main()
