#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

HEADING_BLACKLIST = {
    'theme',
    'short overview',
    'ranked papers',
    'most relevant to cabbageland',
    'novelty / framing / baseline impact',
    'one-paragraph takeaway',
    'detailed notes',
    'basic info',
    'model definition',
    'key questions this summary must address',
    'inputs',
    'outputs',
    'training objective (loss)',
    'architecture / parameterization',
    'quick verdict',
}

BANNED_AUDIO_PHRASES = [
    'Daily Paper Digest —',
    'Daily Digest —',
    'Basic info',
    'Model definition',
    'Key questions this summary must address',
    'This section is mandatory whenever the paper contains',
    'Theme',
    'Short overview',
    'Ranked papers',
    'Detailed notes',
]

ROOT = Path(__file__).resolve().parent
WEB_ROOT = ROOT.parent / 'cabbageclaw-paper-daily-web'
VENV_PYTHON = ROOT.parent / '.venv-piper' / 'bin' / 'python'
VOICE_CACHE_DIR = Path.home() / '.cache' / 'piper-voices'
LEGACY_VOICE_DIR = WEB_ROOT / 'audio' / 'voices'
GENERATED_DIR = WEB_ROOT / 'audio' / 'generated'
SCRIPT_DIR = ROOT / 'audio_scripts'
AUDIO_MANIFEST = ROOT / 'audio_manifest.json'
VOICE_NAME = 'en_US-hfc_male-medium'
SPEECH_RATE = 0.95
SILENCE_BETWEEN_CHUNKS_SEC = 0.32


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8').replace('\r\n', '\n')


def strip_inline_markup(text: str) -> str:
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = text.replace('**', '').replace('*', '')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_section(text: str, heading: str) -> str:
    pattern = rf'^## {re.escape(heading)}\n+(.*?)(?=^## |\Z)'
    m = re.search(pattern, text, flags=re.M | re.S)
    return m.group(1).strip() if m else ''


def extract_subsection(text: str, heading: str) -> str:
    pattern = rf'^### {re.escape(heading)}\n+(.*?)(?=^### |^## |\Z)'
    m = re.search(pattern, text, flags=re.M | re.S)
    return m.group(1).strip() if m else ''


def bullet_value(text: str, label: str) -> str:
    m = re.search(rf'^\* {re.escape(label)}:\s*(.+)$', text, flags=re.M)
    return m.group(1).strip() if m else ''


def clean_spoken_line(text: str) -> str:
    text = strip_inline_markup(text)
    text = re.sub(r'\\\((.*?)\\\)', r'\1', text)
    text = re.sub(r'\\\[(.*?)\\\]', r'\1', text)
    text = re.sub(r'\$([^$]+)\$', r'\1', text)
    text = re.sub(r'\\mathcal\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\lambda', 'lambda', text)
    text = re.sub(r'\\[A-Za-z]+', '', text)
    text = text.replace('—', ', ').replace('–', ', ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def spokenize_markdown(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    in_code = False
    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not stripped:
            out.append('')
            continue

        heading = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if heading:
            heading_text = clean_spoken_line(heading.group(2))
            lowered = heading_text.lower().rstrip(':')
            if not heading_text or lowered in HEADING_BLACKLIST or lowered.startswith('daily paper digest') or lowered.startswith('daily digest'):
                continue
            out.append(heading_text)
            out.append('')
            continue

        bullet = re.match(r'^[-*]\s+(.*)$', stripped)
        if bullet:
            content = clean_spoken_line(bullet.group(1))
            if content:
                out.append(content)
            continue

        numbered = re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if numbered:
            content = clean_spoken_line(numbered.group(2))
            if content:
                out.append(content)
            continue

        content = clean_spoken_line(stripped)
        if content.startswith('This section is mandatory whenever the paper contains'):
            continue
        if content in BANNED_AUDIO_PHRASES:
            continue
        if content:
            out.append(content)

    text = '\n'.join(out)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'\s+\n', '\n', text)
    text = re.sub(r'(?m)^\s*[-*]\s*', '', text)
    return text.strip()


def spoken_date(date_str: str) -> str:
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return dt.strftime('%B %d, %Y').replace(' 0', ' ')


def section_paragraphs(section_text: str) -> list[str]:
    if not section_text:
        return []
    blocks = [b.strip() for b in re.split(r'\n\s*\n', section_text) if b.strip()]
    cleaned: list[str] = []
    for block in blocks:
        block = spokenize_markdown(block)
        if block:
            cleaned.append(block)
    return cleaned


def render_digest_body(source: Path) -> str:
    text = read_text(source)
    parts: list[str] = []
    parts.extend(section_paragraphs(extract_section(text, 'Theme')))
    parts.extend(section_paragraphs(extract_section(text, 'Short overview')))
    parts.extend(section_paragraphs(extract_section(text, 'Most relevant to cabbageland')))
    parts.extend(section_paragraphs(extract_section(text, 'Novelty / framing / baseline impact')))
    parts.extend(section_paragraphs(extract_section(text, 'One-paragraph takeaway')))
    return '\n\n'.join(parts).strip()


def render_note_body(source: Path) -> str:
    text = read_text(source)
    parts: list[str] = []

    why_selected = clean_spoken_line(bullet_value(text, 'Why selected in one sentence'))
    verdict_block = extract_section(text, 'Quick verdict')
    verdict_lines = [clean_spoken_line(ln) for ln in verdict_block.splitlines() if clean_spoken_line(ln)]
    if why_selected:
        parts.append(why_selected)
    if verdict_lines:
        if len(verdict_lines) == 1:
            parts.append(verdict_lines[0])
        else:
            parts.append(' '.join(verdict_lines))

    overview = extract_section(text, 'One-paragraph overview')
    if overview:
        parts.extend(section_paragraphs(overview))

    for question_num in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']:
        q = extract_subsection(text, f'{question_num}. What problem is the paper trying to solve?')
        if question_num == '1' and q:
            parts.append(q)
        q = extract_subsection(text, f'{question_num}. What is the method?')
        if question_num == '2' and q:
            parts.append(q)
        q = extract_subsection(text, f'{question_num}. What data does it use?')
        if question_num == '4' and q:
            parts.append(q)
        q = extract_subsection(text, f'{question_num}. What are the main results?')
        if question_num == '6' and q:
            parts.append(q)
        q = extract_subsection(text, f'{question_num}. What is actually novel?')
        if question_num == '7' and q:
            parts.append(q)
        q = extract_subsection(text, f'{question_num}. What are the weaknesses, limitations, or red flags?')
        if question_num == '9' and q:
            parts.append(q)
        q = extract_subsection(text, f'{question_num}. Why does this matter for cabbageland?')
        if question_num == '12' and q:
            parts.append(q)
        q = extract_subsection(text, f'{question_num}. Final decision')
        if question_num == '14' and q:
            parts.append(q)

    cleaned_parts = [spokenize_markdown(p) for p in parts if p and spokenize_markdown(p)]
    return '\n\n'.join(cleaned_parts).strip()


def render_related_body(source: Path) -> str:
    text = read_text(source)
    return spokenize_markdown(text)


def wrap_digest_script(path: Path, body: str) -> str:
    title_prefix = 'Daily Digest' if path.stem == '2026-03-30' else 'Paper Daily'
    opening = f'Welcome to the {spoken_date(path.stem)} {title_prefix} at Cabbageland.'
    closing = 'Your reporter, cabbage claw.'
    return f'{opening}\n\n{body.strip()}\n\n{closing}\n'


def wrap_note_script(title: str, body: str) -> str:
    opening = f'Welcome to the Cabbageland Paper Daily reading notes on {title}.'
    closing = 'Your reporter, cabbage claw.'
    return f'{opening}\n\n{body.strip()}\n\n{closing}\n'


def wrap_related_script(title: str, body: str) -> str:
    opening = f'Welcome to the Cabbageland Paper Daily related work briefing on {title}.'
    closing = 'Your reporter, cabbage claw.'
    return f'{opening}\n\n{body.strip()}\n\n{closing}\n'


def voice_urls(voice_name: str) -> tuple[str, str]:
    parts = voice_name.split('-')
    if len(parts) < 3:
        raise ValueError(f'Unexpected Piper voice name: {voice_name}')
    locale = parts[0]
    speaker = parts[1]
    quality = parts[2]
    base = f'https://huggingface.co/rhasspy/piper-voices/resolve/main/en/{locale}/{speaker}/{quality}/{voice_name}.onnx'
    return f'{base}?download=true', f'{base}.json?download=true'


def resolve_voice_files(voice_name: str) -> tuple[Path, Path]:
    VOICE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    model = VOICE_CACHE_DIR / f'{voice_name}.onnx'
    config = VOICE_CACHE_DIR / f'{voice_name}.onnx.json'
    if model.exists() and config.exists():
        return model, config

    legacy_model = LEGACY_VOICE_DIR / f'{voice_name}.onnx'
    legacy_config = LEGACY_VOICE_DIR / f'{voice_name}.onnx.json'
    if legacy_model.exists() and legacy_config.exists():
        model.write_bytes(legacy_model.read_bytes())
        config.write_bytes(legacy_config.read_bytes())
        return model, config

    model_url, config_url = voice_urls(voice_name)
    for url, out in ((model_url, model), (config_url, config)):
        subprocess.run([
            'python3', '-c',
            (
                'import requests,sys; '
                'url=sys.argv[1]; out=sys.argv[2]; '
                'r=requests.get(url,stream=True,timeout=60); r.raise_for_status(); '
                'f=open(out,"wb"); '
                '[f.write(c) for c in r.iter_content(chunk_size=1024*1024) if c]; f.close()'
            ),
            url,
            str(out),
        ], check=True)
    return model, config


@dataclass
class AudioJob:
    source_path: str
    script_path: Path
    audio_path: Path
    label: str
    kind: str
    title: str


def build_jobs() -> list[AudioJob]:
    jobs: list[AudioJob] = []
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    for path in sorted((ROOT / 'daily_papers').glob('*.md')):
        if path.name == '.gitkeep':
            continue
        jobs.append(AudioJob(
            source_path=f'daily_papers/{path.name}',
            script_path=SCRIPT_DIR / f'{path.stem}_digest_audio_script.md',
            audio_path=GENERATED_DIR / f'{path.stem}_digest.wav',
            label='listen',
            kind='digest',
            title=path.stem,
        ))

    for path in sorted((ROOT / 'paper_notes').glob('*.md')):
        if path.name == '.gitkeep':
            continue
        title = read_text(path).splitlines()[0].removeprefix('#').strip()
        jobs.append(AudioJob(
            source_path=f'paper_notes/{path.name}',
            script_path=SCRIPT_DIR / f'{path.stem}_audio_script.md',
            audio_path=GENERATED_DIR / f'{path.stem}.wav',
            label='listen',
            kind='note',
            title=title,
        ))

    for path in sorted((ROOT / 'related_work').glob('*.md')):
        if path.name == '.gitkeep':
            continue
        title = read_text(path).splitlines()[0].removeprefix('#').strip()
        jobs.append(AudioJob(
            source_path=f'related_work/{path.name}',
            script_path=SCRIPT_DIR / f'{path.stem}_audio_script.md',
            audio_path=GENERATED_DIR / f'{path.stem}.wav',
            label='listen',
            kind='related',
            title=title,
        ))
    return jobs


def render_script(job: AudioJob) -> str:
    source = ROOT / Path(job.source_path)
    if job.kind == 'digest':
        return wrap_digest_script(source, render_digest_body(source))
    if job.kind == 'note':
        return wrap_note_script(job.title, render_note_body(source))
    return wrap_related_script(job.title, render_related_body(source))


def validate_script(job: AudioJob, script: str) -> None:
    if 'http://' in script or 'https://' in script:
        raise ValueError(f'{job.script_path.name}: raw URL left in script')
    if script.count('# ') or script.count('## '):
        raise ValueError(f'{job.script_path.name}: markdown headings left in script')
    if job.kind == 'digest' and not script.startswith('Welcome to the '):
        raise ValueError(f'{job.script_path.name}: missing standardized digest opening')
    if job.kind in {'note', 'related'} and not script.startswith('Welcome to the Cabbageland Paper Daily'):
        raise ValueError(f'{job.script_path.name}: missing standardized opening')
    if not script.strip().endswith('Your reporter, cabbage claw.'):
        raise ValueError(f'{job.script_path.name}: missing standardized closing')
    for phrase in BANNED_AUDIO_PHRASES:
        if phrase in script:
            raise ValueError(f'{job.script_path.name}: banned phrase leaked into script: {phrase}')
    if '\\(' in script or '\\[' in script or '$' in script or '\\mathcal' in script:
        raise ValueError(f'{job.script_path.name}: math/latex-like markup left in script')


def write_scripts(jobs: Iterable[AudioJob]) -> None:
    for job in jobs:
        script = render_script(job)
        validate_script(job, script)
        job.script_path.write_text(script, encoding='utf-8')


def synthesize(jobs: Iterable[AudioJob]) -> None:
    jobs_list = list(jobs)
    voice_model, voice_config = resolve_voice_files(VOICE_NAME)
    script = f'''
import wave
from pathlib import Path
from piper.voice import PiperVoice
from piper.config import SynthesisConfig
voice = PiperVoice.load(r"{voice_model}", r"{voice_config}")
config = SynthesisConfig(length_scale={1 / SPEECH_RATE}, noise_scale=0.667, noise_w_scale=0.8)
jobs = {[(str(j.script_path), str(j.audio_path)) for j in jobs_list]!r}
for script_path, out_path in jobs:
    text = Path(script_path).read_text(encoding='utf-8').strip()
    with wave.open(out_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(voice.config.sample_rate)
        first = True
        for chunk in voice.synthesize(text, syn_config=config):
            if not first:
                wav_file.writeframes(b"\\x00\\x00" * int(voice.config.sample_rate * {SILENCE_BETWEEN_CHUNKS_SEC}))
            wav_file.writeframes(chunk.audio_int16_bytes)
            first = False
    print('wrote', out_path)
'''
    subprocess.run([str(VENV_PYTHON), '-c', script], check=True)


def update_manifest(jobs: Iterable[AudioJob]) -> None:
    data = {
        'voice': VOICE_NAME,
        'rate': SPEECH_RATE,
        'items': {},
    }
    for job in jobs:
        data['items'][job.source_path] = {
            'label': job.label,
            'scriptPath': str(job.script_path.relative_to(ROOT)),
            'audioPath': str(job.audio_path.relative_to(WEB_ROOT)),
            'voice': VOICE_NAME,
            'rate': SPEECH_RATE,
        }
    AUDIO_MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def main() -> None:
    jobs = build_jobs()
    write_scripts(jobs)
    synthesize(jobs)
    update_manifest(jobs)
    print(f'generated {len(jobs)} audio items')


if __name__ == '__main__':
    main()
