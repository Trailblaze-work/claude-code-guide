#!/usr/bin/env python3
"""Generate the Trailblaze brand image (mark + wordmark) from source SVGs.

Requirements:
    - rsvg-convert (brew install librsvg)
    - Pillow (pip install Pillow)

Source files (in this directory):
    - trailblaze-mark.svg   (symlink to ../trailblaze.work/trailblaze-mark.svg)
    - trailblaze-wordmark.svg

Outputs:
    - trailblaze-brand.png   (combined mark + wordmark, for PDF cover)
    - trailblaze-mark.png    (standalone mark, 128x128)
    - trailblaze-wordmark.png (standalone wordmark)
"""

import os
import subprocess
import tempfile

from PIL import Image

_HERE = os.path.dirname(os.path.abspath(__file__))

# ── Config ──────────────────────────────────────────────────────────────
MARK_SVG = os.path.join(_HERE, "trailblaze-mark.svg")
WORDMARK_SVG = os.path.join(_HERE, "trailblaze-wordmark.svg")

FLAME_RENDER_SIZE = 1024          # render mark SVG at this resolution
WORDMARK_RENDER_WIDTH = 4000      # render wordmark SVG at this width
FLAME_HEIGHT_RATIO = 1.575        # flame height as multiple of wordmark height
FLAME_Y_SHIFT = -0.1             # vertical offset as fraction of wordmark height (negative = up)
GAP_RATIO = 0.25                  # gap between mark and wordmark as fraction of wordmark height
STANDALONE_MARK_SIZE = 128        # standalone mark output size


def rsvg_convert(svg_path, out_path, width=None, height=None):
    cmd = ["rsvg-convert", svg_path, "-o", out_path]
    if width:
        cmd += ["-w", str(width)]
    if height:
        cmd += ["-h", str(height)]
    subprocess.run(cmd, check=True)


def generate():
    with tempfile.TemporaryDirectory() as tmp:
        # Render mark SVG at high resolution
        flame_png = os.path.join(tmp, "flame.png")
        rsvg_convert(MARK_SVG, flame_png, width=FLAME_RENDER_SIZE, height=FLAME_RENDER_SIZE)

        # Render wordmark SVG
        wordmark_png = os.path.join(tmp, "wordmark.png")
        rsvg_convert(WORDMARK_SVG, wordmark_png, width=WORDMARK_RENDER_WIDTH)

        # Load and crop to content
        flame = Image.open(flame_png)
        flame = flame.crop(flame.getbbox())

        wordmark = Image.open(wordmark_png)
        wordmark = wordmark.crop(wordmark.getbbox())

        # Scale flame relative to wordmark
        target_h = int(wordmark.height * FLAME_HEIGHT_RATIO)
        ratio = target_h / flame.height
        flame_resized = flame.resize(
            (int(flame.width * ratio), target_h), Image.LANCZOS
        )

        # Compose brand image
        gap = int(wordmark.height * GAP_RATIO)
        total_w = flame_resized.width + gap + wordmark.width
        total_h = max(flame_resized.height, wordmark.height)

        combined = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))

        flame_y = (total_h - flame_resized.height) // 2 + int(
            wordmark.height * FLAME_Y_SHIFT
        )
        combined.paste(flame_resized, (0, max(0, flame_y)), flame_resized)

        word_y = (total_h - wordmark.height) // 2
        combined.paste(
            wordmark, (flame_resized.width + gap, word_y), wordmark
        )

        combined = combined.crop(combined.getbbox())

        # Save outputs
        brand_out = os.path.join(_HERE, "trailblaze-brand.png")
        combined.save(brand_out)
        print(f"Brand image: {brand_out} ({combined.size[0]}x{combined.size[1]})")

        wordmark_out = os.path.join(_HERE, "trailblaze-wordmark.png")
        wordmark.save(wordmark_out)
        print(f"Wordmark:    {wordmark_out} ({wordmark.size[0]}x{wordmark.size[1]})")

        mark_out = os.path.join(_HERE, "trailblaze-mark.png")
        rsvg_convert(MARK_SVG, mark_out, width=STANDALONE_MARK_SIZE, height=STANDALONE_MARK_SIZE)
        print(f"Mark:        {mark_out} ({STANDALONE_MARK_SIZE}x{STANDALONE_MARK_SIZE})")


if __name__ == "__main__":
    generate()
