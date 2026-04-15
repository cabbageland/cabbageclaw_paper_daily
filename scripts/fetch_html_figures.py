#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER_NOTES = ROOT / 'paper_notes'
ASSETS_DIR = ROOT / 'assets' / 'html_figures'


class FigureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_figure = False
        self.in_caption = False
        self.current: dict | None = None
        self.figures: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == 'figure':
            self.in_figure = True
            self.current = {
                'id': attr_map.get('id') or '',
                'imgs': [],
                'caption': '',
            }
        elif self.in_figure and tag == 'img' and self.current is not None:
            src = attr_map.get('src')
            if src:
                self.current['imgs'].append(src)
        elif self.in_figure and tag == 'figcaption':
            self.in_caption = True

    def handle_endtag(self, tag: str) -> None:
        if tag == 'figcaption':
            self.in_caption = False
        elif tag == 'figure' and self.in_figure:
            self.in_figure = False
            if self.current is not None:
                self.current['caption'] = re.sub(r'\s+', ' ', self.current['caption']).strip()
                self.figures.append(self.current)
            self.current = None

    def handle_data(self, data: str) -> None:
        if self.in_figure and self.in_caption and self.current is not None:
            self.current['caption'] += data


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8').replace('\r\n', '\n')


def note_link(note_path: Path) -> str:
    text = read_text(note_path)
    m = re.search(r'^\* Link:\s*(.+)$', text, flags=re.M)
    if not m:
        raise ValueError(f'No Link bullet found in {note_path.name}')
    return m.group(1).strip()


def arxiv_abs_id(url: str) -> str:
    m = re.search(r'arxiv\.org/abs/([0-9]+\.[0-9]+)', url)
    if not m:
        raise ValueError(f'Unsupported link for HTML figure fetch: {url}')
    return m.group(1)


def fetch_html(abs_id: str) -> str:
    with urllib.request.urlopen(f'https://arxiv.org/html/{abs_id}', timeout=30) as resp:
        return resp.read().decode('utf-8', 'ignore')


def pick_target_figures(figures: list[dict], wanted: list[str]) -> list[dict]:
    out = []
    for name in wanted:
        prefix = f'{name}:'
        for fig in figures:
            cap = fig.get('caption', '')
            if cap.startswith(prefix):
                out.append(fig)
                break
        else:
            raise ValueError(f'Could not find {name} in fetched HTML figures')
    return out


def absolute_img_url(abs_id: str, src: str) -> str:
    if src.startswith('http://') or src.startswith('https://'):
        return src
    return f'https://arxiv.org/html/{src.lstrip("/")}' if src.startswith('/') else f'https://arxiv.org/html/{src}'


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=30) as resp:
        dest.write_bytes(resp.read())


def replace_figure_section(note_path: Path, asset_prefix: str, figures: list[dict]) -> None:
    text = read_text(note_path)
    block_lines = ['## Key figures from HTML', '']
    for idx, fig in enumerate(figures, start=1):
        caption = fig['caption']
        number = re.match(r'^(Figure\s+\d+):\s*(.*)$', caption)
        title = number.group(1) if number else f'Figure {idx}'
        summary = number.group(2).strip() if number else caption.strip()
        image_name = f'{asset_prefix}_fig{idx}.png'
        rel_path = f'../assets/html_figures/{image_name}'
        block_lines.extend([
            f'### {title}',
            f'![{title} from the paper]({rel_path})',
            '',
            f'Caption summary: {summary}',
            '',
        ])
    new_block = '\n'.join(block_lines).rstrip() + '\n'
    pattern = r'\n## Key figures from HTML\n.*?(?=\n## |\Z)'
    if re.search(pattern, text, flags=re.S):
        updated = re.sub(pattern, lambda _m: '\n' + new_block, text, flags=re.S)
    else:
        updated = text.rstrip() + '\n\n' + new_block
    note_path.write_text(updated, encoding='utf-8')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('note', help='paper note filename, with or without .md')
    ap.add_argument('--figures', nargs='+', required=True, help='Figure labels to fetch, e.g. "Figure 1" "Figure 2"')
    args = ap.parse_args()

    note_name = args.note if args.note.endswith('.md') else f'{args.note}.md'
    note_path = PAPER_NOTES / note_name
    if not note_path.exists():
        raise SystemExit(f'Note not found: {note_path}')

    url = note_link(note_path)
    abs_id = arxiv_abs_id(url)
    html = fetch_html(abs_id)
    parser = FigureParser()
    parser.feed(html)
    figures = pick_target_figures(parser.figures, args.figures)

    asset_prefix = note_path.stem
    for idx, fig in enumerate(figures, start=1):
        srcs = fig.get('imgs') or []
        if not srcs:
            raise SystemExit(f'{args.figures[idx-1]} has no image src in HTML')
        url = absolute_img_url(abs_id, srcs[0])
        dest = ASSETS_DIR / f'{asset_prefix}_fig{idx}.png'
        download(url, dest)
        print(f'downloaded {url} -> {dest}')

    replace_figure_section(note_path, asset_prefix, figures)
    print(f'updated {note_path}')


if __name__ == '__main__':
    main()
