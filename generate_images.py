#!/usr/bin/env python3
"""
The Relay — Image Generator (fal.ai nano-banana-2, text-to-image)
Reads approved concepts from L3-approved-concepts.md (written by the relay).
Generates images using fal-ai/nano-banana-2.

Requires: FAL_KEY environment variable (get one at fal.ai)

Usage:
    FAL_KEY=your_key python generate_images.py
"""

import json
import os
import time
import re
import urllib.request
from pathlib import Path
from datetime import datetime

import fal_client

# Config — set FAL_KEY in your environment before running
FAL_KEY = os.environ.get("FAL_KEY")
if not FAL_KEY:
    raise SystemExit("FAL_KEY environment variable not set. Get a key at fal.ai and run: export FAL_KEY=your_key")
os.environ["FAL_KEY"] = FAL_KEY

BASE_DIR = Path(__file__).parent
APPROVED_CONCEPTS_PATH = BASE_DIR / "artifacts" / "L3-approved-concepts.md"
OUTPUT_DIR = BASE_DIR / "images"
LOG_PATH = BASE_DIR / "artifacts" / "L4-generation-log.md"

OUTPUT_DIR.mkdir(exist_ok=True)

# Parse approved concepts from markdown
# Expected format per concept:
#   ## [Concept Name]
#   **Prompt:** <generation prompt text>
#   **Negative:** <negative prompt — optional>

def parse_concepts(md_path):
    text = md_path.read_text()
    concepts = []
    blocks = re.split(r'\n##\s+', text)
    for block in blocks[1:]:  # skip preamble
        lines = block.strip().split('\n')
        name = lines[0].strip()
        prompt = ""
        negative = ""
        for line in lines[1:]:
            if line.startswith("**Prompt:**"):
                prompt = line.replace("**Prompt:**", "").strip()
            elif line.startswith("**Negative:**"):
                negative = line.replace("**Negative:**", "").strip()
        if name and prompt:
            slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            concepts.append({"name": name, "slug": slug, "prompt": prompt, "negative": negative})
    return concepts

concepts = parse_concepts(APPROVED_CONCEPTS_PATH)
print(f"Found {len(concepts)} approved concepts:")
for c in concepts:
    print(f"  - {c['name']}")

# Generate
log_lines = [
    f"# L4 — Image Generation Log",
    f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    f"Model: fal-ai/nano-banana-2",
    f"Concepts: {len(concepts)}",
    "---\n"
]

success_count = 0
failed = []

for i, concept in enumerate(concepts, 1):
    output_path = OUTPUT_DIR / f"{concept['slug']}-{i:02d}.png"
    print(f"\n[{i}/{len(concepts)}] {concept['name']}")
    print(f"  Prompt: {concept['prompt'][:100]}...")

    try:
        result = fal_client.subscribe(
            "fal-ai/nano-banana-2",
            arguments={
                "prompt": concept["prompt"],
                "negative_prompt": concept["negative"] or "text, watermark, logo, brand name, low quality, blurry",
                "aspect_ratio": "4:5",
                "num_images": 1,
            }
        )

        # Extract image URL
        img_url = None
        if hasattr(result, 'images') and result.images:
            img_url = result.images[0].url
        elif isinstance(result, dict):
            if 'images' in result and result['images']:
                img_url = result['images'][0]['url'] if isinstance(result['images'][0], dict) else result['images'][0].url

        if img_url:
            urllib.request.urlretrieve(img_url, output_path)
            print(f"  Saved: {output_path.name}")
            log_lines.append(f"## {concept['name']}")
            log_lines.append(f"**Status:** GENERATED")
            log_lines.append(f"**File:** {output_path.name}")
            log_lines.append(f"**Prompt:** {concept['prompt']}")
            log_lines.append("")
            success_count += 1
        else:
            raise ValueError(f"No image URL in result: {result}")

    except Exception as e:
        print(f"  ERROR: {e}")
        failed.append({"name": concept["name"], "error": str(e)})
        log_lines.append(f"## {concept['name']}")
        log_lines.append(f"**Status:** FAILED")
        log_lines.append(f"**Error:** {e}")
        log_lines.append("")

    time.sleep(2)

# Summary
log_lines.append("---")
log_lines.append(f"## Summary")
log_lines.append(f"**Generated:** {success_count}/{len(concepts)}")
if failed:
    log_lines.append(f"**Failed:** {len(failed)}")
    for f in failed:
        log_lines.append(f"  - {f['name']}: {f['error']}")

LOG_PATH.write_text('\n'.join(log_lines))

print(f"\n{'='*50}")
print(f"Done. {success_count}/{len(concepts)} images generated.")
print(f"Images: {OUTPUT_DIR}")
print(f"Log: {LOG_PATH}")
