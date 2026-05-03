# The Relay

Autonomous image ad relay for Claude Code. Point it at a funnel, walk away. Come back to a folder of ads.

## How it works

The relay runs as a sequence of legs. Each leg is a fresh Claude instance with clean context — no baggage from previous legs. It reads the baton (a file), runs its job, writes its output, hands off, and exits. The next instance picks up.

```
L1 — Concept Selection    reads funnel → picks formats from swipe file
L2 — Image Briefs         writes scene descriptions with built-in contradictions
L3 — Quality Gate         3-gate check: contradiction / pause / not-stock
L4 — Image Generation     generates images via fal.ai
```

The output is a folder of images. No human in the loop after kickoff.

## Requirements

- [Claude Code](https://claude.ai/code) with `--dangerously-skip-permissions`
- Python 3.9+
- `pip install fal-client`
- A fal.ai API key — get one at [fal.ai](https://fal.ai)

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/theprompted/relay.git
cd relay

# 2. Install dependencies
pip install fal-client

# 3. Set your fal.ai key
export FAL_KEY=your_key_here

# 4. Copy the template and configure it
cp relay.template.json relay.json
```

Edit `relay.json`:
- Set `funnel` to your landing page URL
- Set `outputDir` to an absolute path where outputs should be saved (e.g. `/Users/you/relay-run`)
- Set `adCount` to how many concepts you want (5 is a good start)
- Update L1 `acceptanceCriteria` to select the right number of concepts
- Update L3 target to match

## Run

```bash
mkdir -p /your/output/dir/artifacts /your/output/dir/images
cp generate_images.py /your/output/dir/
cp RELAY.md /your/output/dir/
cp relay.json /your/output/dir/
cd /your/output/dir && bash /path/to/relay/relay.sh 10 2>&1 | tee relay-output.log
```

Or use the `/relay-lite` Claude Code skill if you have it installed — it handles setup automatically.

## What's in the swipe file

`ad-formats-lite.json` contains 30 curated ad formats across 15 format families:

UGC · Testimonial · Native Advertorial · Problem-Agitate · Before/After · Authority · Myth Buster · Us-vs-Them · Pattern Interrupt · Founder · Platform Mimicry · Social Proof · Benefit Callout · Timeline · Objection Handling

The relay uses these as the starting point for concept selection — it picks the formats that best match your specific funnel and avatar, not generic formats.

## Output structure

```
your-output-dir/
  artifacts/
    L1-concept-selection.md
    L2-image-concepts.md
    L3-approved-concepts.md
    L4-generation-log.md
  images/
    concept-name-01.png
    concept-name-02.png
    ...
  baton.txt
  relay.json
  relay-output.log
```

## The quality gate (L3)

Every image concept is run through three gates before it gets generated:

1. **Contradiction check** — does the image carry its own contradiction without any text?
2. **Pause check** — would someone stop scrolling on this image with no copy visible?
3. **Stock check** — does this look like a real photo, not a stock image?

All three must pass. Concepts that fail are documented and cut. This is what makes the output usable.

## Cost

Each image costs roughly $0.003–0.01 on fal.ai using `fal-ai/nano-banana-2`. A 5-concept run costs under $0.10.

Claude Code usage (L1–L3) is covered by your Claude subscription.

## License

MIT
