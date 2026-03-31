#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT.parent / 'cabbageclaw-paper-daily-web'
MANIFEST = ROOT / 'audio_manifest.json'
CONTENT = WEB / 'data' / 'content.json'
WEB_AUDIO = WEB / 'audio' / 'generated'
DAILY_DIR = ROOT / 'daily_papers'


def fail(msg: str) -> None:
    print(f'ERROR: {msg}', file=sys.stderr)
    raise SystemExit(1)


def newest_digest_key() -> str:
    digests = sorted(p.stem for p in DAILY_DIR.glob('*.md') if p.name != '.gitkeep')
    if not digests:
        fail('no daily digests found')
    return f'daily_papers/{digests[-1]}.md'


def main() -> None:
    key = newest_digest_key()
    if not MANIFEST.exists():
        fail(f'missing manifest: {MANIFEST}')
    if not CONTENT.exists():
        fail(f'missing web content snapshot: {CONTENT}')

    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    content = json.loads(CONTENT.read_text(encoding='utf-8'))

    manifest_item = manifest.get('items', {}).get(key)
    if not manifest_item:
        fail(f'{key} missing from audio_manifest.json')

    content_item = content.get('audio', {}).get(key)
    if not content_item:
        fail(f'{key} missing from web data/content.json audio section')

    audio_path = WEB / manifest_item['audioPath']
    if not audio_path.exists():
        fail(f'missing audio file: {audio_path}')
    if audio_path.stat().st_size <= 0:
        fail(f'empty audio file: {audio_path}')

    print(f'OK: {key}')
    print(f'  manifest -> {manifest_item["audioPath"]}')
    print(f'  web data -> present')
    print(f'  audio file -> {audio_path} ({audio_path.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
