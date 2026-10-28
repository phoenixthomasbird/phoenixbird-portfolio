#!/usr/bin/env python3
"""
add_margins.py
Adds white margins around every page of a PDF without re-encoding content.
Each source page is placed as a form XObject on a larger blank canvas.

Usage:
    python3 add_margins.py                         # uses defaults below
    python3 add_margins.py --input /path/to/in.pdf --output /path/to/out.pdf --margin 0.75
"""

import argparse
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# ── DEFAULTS ──────────────────────────────────────────────────────────────────
DEFAULT_INPUT  = "input.pdf"
DEFAULT_OUTPUT = "output_margins.pdf"
DEFAULT_MARGIN = 0.5   # inches — change to whatever you need (0.5, 0.75, 1.0)
# ──────────────────────────────────────────────────────────────────────────────

def inches_to_pt(inches: float) -> float:
    return inches * 72.0


def add_margins_to_pdf(input_path: str, output_path: str, margin_in: float) -> None:
    margin_pt = inches_to_pt(margin_in)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    total = len(reader.pages)
    print(f"Source: {input_path}")
    print(f"Pages:  {total}")
    print(f"Margin: {margin_in}\" ({margin_pt:.1f}pt) on all sides")
    print(f"Output: {output_path}")
    print()

    for i, src_page in enumerate(reader.pages):
        # Source page dimensions in points
        src_w = float(src_page.mediabox.width)
        src_h = float(src_page.mediabox.height)

        # New canvas size = source + margin on all 4 sides
        new_w = src_w + margin_pt * 2
        new_h = src_h + margin_pt * 2

        # --- Build a blank page at the new size via reportlab ---
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(new_w, new_h))
        # White background (default canvas is white, this makes it explicit)
        c.setFillColorRGB(1, 1, 1)
        c.rect(0, 0, new_w, new_h, fill=1, stroke=0)
        c.save()
        packet.seek(0)

        # Read the blank canvas page
        blank_reader = PdfReader(packet)
        blank_page = blank_reader.pages[0]

        # Merge the source page onto the blank canvas at the margin offset
        # merge_transformed_page places src_page translated by (margin_pt, margin_pt)
        blank_page.merge_transformed_page(
            src_page,
            ctm=Transformation().translate(tx=margin_pt, ty=margin_pt)
        )

        writer.add_page(blank_page)

        if (i + 1) % 10 == 0 or (i + 1) == total:
            print(f"  Processed {i+1}/{total} pages...")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        writer.write(f)

    print(f"\nDone. Output written to:\n  {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Add margins to a PDF.")
    parser.add_argument("--input",  default=DEFAULT_INPUT,  help="Path to source PDF")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path for output PDF")
    parser.add_argument("--margin", default=DEFAULT_MARGIN, type=float,
                        help="Margin in inches (default: 0.5)")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"ERROR: Input file not found: {args.input}")
        sys.exit(1)

    add_margins_to_pdf(args.input, args.output, args.margin)


if __name__ == "__main__":
    main()