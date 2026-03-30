# TTS Conversion Instructions for Paper Daily Research Briefings

## Purpose

Convert paper-daily digests, paper notes, and related-work docs into spoken briefings that are:
- easy for a text-to-speech model to read cleanly,
- easy for a listener to follow in one pass,
- faithful to the source,
- stripped of visual-only clutter,
- and optimized for oral comprehension rather than markdown layout.

The goal is not to preserve page structure. The goal is to preserve judgment, mechanism, and uncertainty while making the result actually listenable.

## Core Principle

Treat the source document as material for a concise research briefing, not as text to be read aloud verbatim.

The script should sound like a sharp private update on papers about world models, memory, planning, embodied intelligence, structured generation, controllability, and adjacent research areas that matter to cabbageland.

## Fixed Opening and Closing Rules

### Rule 0A. Use the standard digest opening

Every daily digest script must begin with:

**Welcome to the [MONTH DATE, YEAR] Paper Daily at Cabbageland.**

Use spoken date style.

### Rule 0B. Use the standard note opening

Every paper note script should begin with:

**Welcome to the Cabbageland Paper Daily reading notes on [TITLE].**

### Rule 0C. Use the standard related-work opening

Every related-work script should begin with:

**Welcome to the Cabbageland Paper Daily related work briefing on [TITLE].**

### Rule 0D. Always use the standard closing line

Every script must end with:

**Your reporter, cabbage claw.**

## Primary Objectives

Optimize for:

1. Speakability
2. Listenability
3. Fidelity
4. Redundancy reduction
5. TTS robustness
6. Audio flow

## Non-Negotiable Rules

### Rule 1. Preserve meaning, not formatting

Do not preserve raw markdown syntax, bullet indentation, citation syntax, or hyperlinks.

Do preserve:
- verdicts,
- mechanism claims,
- what is actually novel,
- what is decorative,
- what evidence was inspected,
- and what caveats remain.

### Rule 2. Convert written structure into spoken structure

Prefer this flow:

1. standard opening
2. top-line judgment
3. ranked items or key sections
4. why it matters
5. caveats / inspection limits
6. standard closing

### Rule 3. Remove redundancy aggressively

Merge repeated paper titles, repeated verdict language, repeated “why it matters” lines, and repeated takeaways unless the repetition helps oral clarity.

### Rule 4. Make titles explicitly speakable

Introduce titles with spoken framing such as:
- “The first paper is titled...”
- “The most relevant paper today is titled...”
- “Another useful paper is titled...”

### Rule 5. Replace visual shorthand with spoken equivalents

Expand abbreviations on first mention when that improves comprehension.

Examples:
- VLA to vision-language-action model
- VLM to vision-language model
- MPC to model predictive control
- CEM to cross-entropy method
- 3DGS to three-dimensional Gaussian splatting

### Rule 6. Eliminate raw link and citation noise

Never leave in:
- full URLs
- DOI strings
- markdown links
- repository paths
- raw arXiv identifiers without context

Replace them with source-confidence phrasing such as:
- “I inspected the abstract and method text.”
- “This was judged from accessible arXiv HTML only.”
- “I did not audit the appendices in full.”

### Rule 7. Turn bullets into oral prose

Bullets should become short spoken paragraphs or explicit transitions like:
- “First...”
- “Second...”
- “The main caveat is...”

### Rule 8. Keep sentence length under control

Prefer short to medium sentences. One mechanism claim per sentence is usually better than stacking three.

## Research-Specific Guidance

Paper Daily audio should preserve the repo’s actual taste:

- reward mechanism over branding
- separate explicit structure from renamed mush
- keep planning, memory, representation, and controllability claims concrete
- say when a paper is mainly benchmark dressing
- distinguish direct relevance from adjacent inspiration
- do not sand off skepticism for the sake of a smoother narration

If a paper is mainly useful for framing, baselines, or novelty positioning rather than for architecture stealing, say that clearly in the audio too.

## Voice and Delivery Defaults

- default Piper voice: `en_US-hfc_male-medium`
- default rate: `0.95`
- prefer calm, sharp delivery over theatrical emphasis
- preserve uncertainty and inspection limits
- do not exaggerate because audio can make claims sound firmer than they are on the page
