# cabbageclaw_paper_daily

A curated research scouting repository for cabbageland.

This repo is not a paper landfill. It exists to track recent work with actual judgment: selective scouting, sharp notes, transferable mechanisms, and cleaner research taste than the average hype feed.

The point is simple:

- find recent papers worth attention,
- reject weak adjacency,
- extract the mechanism,
- say what is actually novel,
- say what is decorative nonsense,
- preserve the useful bits in a repository that reduces future cognitive load.

## What this repo does

On a good day, the workflow:

1. searches recent papers relevant to cabbageland's research taste,
2. filters aggressively,
3. ranks 5 daily recommendations,
4. writes a compact daily digest,
5. creates structured paper notes for papers that actually matter,
6. updates topic-level synthesis notes when patterns emerge,
7. commits and pushes the result when credentials and permissions exist.

The standard is not volume. The standard is judgment.

## What cabbageland tends to care about

This repository prioritizes papers around:

- world models
- generative models
- 3D / 4D generation
- embodied intelligence
- compositional reasoning
- structured representations
- continual learning
- uncertainty quantification, calibration, verification, and decision-making under uncertainty
- memory, planning, and tool use
- controllability and interpretability
- neurosymbolic or hybrid systems
- neurosymbolic memory and continual learning in VLA / VLM / world models
- mechanism-rich agentic systems
- foundation-model technical reports and serious field-deployment documentation

Robotics and VLA work are one important lane, not the house style. The digest should deliberately keep room for strong non-robotics work: medical, healthcare, neuro, evaluation, interpretability, uncertainty, continual learning, foundation-model reports, field deployment, scientific ML, 3D/generative media, and representation learning.

These topics matter most when the paper improves one of the following:

- structure over mush
- control over vibes
- reusable abstractions over one-off tricks
- explicit state over short-context imitation
- decomposition that actually changes the computation
- evaluation that tests mechanism instead of aesthetic confidence

## What this repo refuses to be

This repo is **not**:

- a dump of every relevant-looking title,
- a benchmark scrapbook,
- a summary mill that rewrites abstracts,
- a politeness machine that calls everything promising,
- a fake "agentic" fan club.

If nothing good appears on a given day, the correct output is: nothing worth logging.

## Repository structure

### `daily_papers/`
Daily digests with ranking, verdicts, and a one-paragraph synthesis.

### `paper_notes/`
Structured, single-paper notes with explicit verdicts, mechanism analysis, weaknesses, and steal-worthy ideas.

### `related_work/`
Cross-paper synthesis notes organized around real research lenses rather than keyword buckets.

### `reading_queue/`
Optional prioritized reading lists when follow-up is warranted.

## Writing standard

The writing here should be:

- direct
- skeptical
- compact
- high-signal
- concrete
- unembarrassing

It should avoid:

- generic praise
- abstract filler
- novelty inflation
- citation theater
- pretending a paper is deeper than it is

## Operating principle

> optimize for research judgment, not paper throughput.

A good day is not twenty weak summaries.
A good day is 5 ranked recommendations with honest judgment, where only the strongest subset earns full notes.

## Automation note

This repository is designed for recurring updates. The detailed workflow and quality bar live in [`TASK.md`](./TASK.md).

If audio transcripts are generated for digests, notes, or related-work briefings, they must be written as spoken research briefings rather than markdown read aloud: clean spoken prose, strong information flow, no literal markdown artifacts, and the standardized Paper Daily Piper voice/rate unless explicitly overridden.

Detailed conversion rules for turning markdown into TTS-friendly spoken scripts live in [`tts_conversion_instructions.md`](./tts_conversion_instructions.md). Treat that file as the default style guide for future digest and note audio-script generation.

## Daily email workflow

The repo includes `paper_daily_email.py`, which renders and sends the same-day Paper Daily digest email using Python SMTP instead of Himalaya's send path.

Behavior:

- subject format: `Paper Daily, [DATE], Reporter: cabbageclaw`
- reads recipients from `recipients.csv` (one email per line)
- supports `--internal-test` mode, which sends only to `recipients-internal-test.csv`
- keeps `recipients.csv` out of git via `.gitignore`
- keeps `recipients-internal-test.csv` out of git via `.gitignore`
- derives preserved-note links from the current digest's `Detailed notes` section and the linked note files
- sends multipart email with both plain-text and HTML versions
- uses a bold HTML signoff block for `Yours,` / `cabbageclaw 🥬🐾`
- expects SMTP settings and password command in `~/.config/himalaya/config.toml`
- runs rule-based QC before send, including exact 5-paper ranking checks, note-body presence, missing `Why it matters` lines, raw markdown leakage, expected hyperlink count, and multipart/alternative structure
- runs a recipient-privacy gate before send: one generated message per recipient, exactly one `To`, no `Cc`/`Bcc`, and no recipient address in the rendered body
- redacts all email addresses from `--dry-run` output and preview `.eml` files
- records send state as recipient counts and hashed fingerprints, never raw recipient addresses
- verifies the live Paper Daily site before send by checking both the homepage and live `data/content.json` markdown coverage for the digest and linked notes

Examples:

```bash
python3 paper_daily_email.py --date 2026-07-16 --dry-run
python3 paper_daily_email.py --date 2026-07-16 --preview-path paper_daily_email_preview.eml
python3 paper_daily_email.py --date 2026-07-16 --internal-test
python3 paper_daily_email.py
```

The intended cron schedule is after the daily publish completes and the live web snapshot has updated. For debugging or maintenance, prefer `--internal-test` so only internal recipients receive the message.
