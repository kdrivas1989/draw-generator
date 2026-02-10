#!/usr/bin/env python3
"""
Extract individual formation cards from the USPA 4-Way Formations PDF.
"""

import os
from pdf2image import convert_from_path
from PIL import Image

# Configuration
PDF_PATH = "/Users/kevindrivas/Desktop/FS Formation Cards/4 way formations.pdf"
OUTPUT_DIR = "/Users/kevindrivas/Desktop/projects/draw-generator/static/formations"

# DPI for high quality extraction
DPI = 300

# Page dimensions at 300 DPI: 2550 x 3300

# Block sequences layout (pages 1-3):
# - Header: ~0-280 pixels
# - Content area: ~280-3180 pixels
# - Footer: ~3180-3300 pixels
# - 4 columns, 2 rows of blocks per page (pages 1-2)
# - Page 3 has blocks 17-22 in a different layout

# Approximate coordinates for blocks on page 1 (will need fine-tuning)
# Each block card is roughly 600x1400 pixels

def extract_block_formations(pages):
    """Extract block sequence formations (1-22)."""

    # Page 1: Blocks 1-8 (4 columns x 2 rows)
    page1 = pages[0]

    # Define crop regions for page 1
    # Format: (left, top, right, bottom)
    # Header ends around y=280, content starts there
    # Each column is about 600 pixels wide
    # Each row (block) is about 1400 pixels tall

    header_offset = 380  # Start below the "Appendix C" header text
    col_width = 600
    row_height = 1340  # Height of each block card
    left_margin = 72

    page1_blocks = {
        1: (left_margin, header_offset, left_margin + col_width, header_offset + row_height),
        2: (left_margin + col_width, header_offset, left_margin + 2*col_width, header_offset + row_height),
        3: (left_margin + 2*col_width, header_offset, left_margin + 3*col_width, header_offset + row_height),
        4: (left_margin + 3*col_width, header_offset, left_margin + 4*col_width, header_offset + row_height),
        5: (left_margin, header_offset + row_height, left_margin + col_width, header_offset + 2*row_height),
        6: (left_margin + col_width, header_offset + row_height, left_margin + 2*col_width, header_offset + 2*row_height),
        7: (left_margin + 2*col_width, header_offset + row_height, left_margin + 3*col_width, header_offset + 2*row_height),
        8: (left_margin + 3*col_width, header_offset + row_height, left_margin + 4*col_width, header_offset + 2*row_height),
    }

    for block_num, coords in page1_blocks.items():
        cropped = page1.crop(coords)
        output_path = os.path.join(OUTPUT_DIR, f"FS-{block_num}.png")
        cropped.save(output_path, "PNG")
        print(f"Saved Block {block_num} to {output_path}")

    # Page 2: Blocks 9-16
    page2 = pages[1]
    page2_header = 240  # Different header on subsequent pages

    page2_blocks = {
        9: (left_margin, page2_header, left_margin + col_width, page2_header + row_height),
        10: (left_margin + col_width, page2_header, left_margin + 2*col_width, page2_header + row_height),
        11: (left_margin + 2*col_width, page2_header, left_margin + 3*col_width, page2_header + row_height),
        12: (left_margin + 3*col_width, page2_header, left_margin + 4*col_width, page2_header + row_height),
        13: (left_margin, page2_header + row_height, left_margin + col_width, page2_header + 2*row_height),
        14: (left_margin + col_width, page2_header + row_height, left_margin + 2*col_width, page2_header + 2*row_height),
        15: (left_margin + 2*col_width, page2_header + row_height, left_margin + 3*col_width, page2_header + 2*row_height),
        16: (left_margin + 3*col_width, page2_header + row_height, left_margin + 4*col_width, page2_header + 2*row_height),
    }

    for block_num, coords in page2_blocks.items():
        cropped = page2.crop(coords)
        output_path = os.path.join(OUTPUT_DIR, f"FS-{block_num}.png")
        cropped.save(output_path, "PNG")
        print(f"Saved Block {block_num} to {output_path}")

    # Page 3: Blocks 17-22
    # First row (17-20): 4 blocks in standard layout
    # Second row (21-22): 2 wider blocks
    page3 = pages[2]
    page3_header = 240

    # Blocks 17-20 in first row
    page3_blocks_row1 = {
        17: (left_margin, page3_header, left_margin + col_width, page3_header + row_height),
        18: (left_margin + col_width, page3_header, left_margin + 2*col_width, page3_header + row_height),
        19: (left_margin + 2*col_width, page3_header, left_margin + 3*col_width, page3_header + row_height),
        20: (left_margin + 3*col_width, page3_header, left_margin + 4*col_width, page3_header + row_height),
    }

    for block_num, coords in page3_blocks_row1.items():
        cropped = page3.crop(coords)
        output_path = os.path.join(OUTPUT_DIR, f"FS-{block_num}.png")
        cropped.save(output_path, "PNG")
        print(f"Saved Block {block_num} to {output_path}")

    # Blocks 21-22 in second row - they each take one standard column width
    # Looking at page 3, blocks 21 and 22 are in a 2-column layout at bottom
    row2_top = page3_header + row_height + 80  # Gap between rows, skip past Murphy/Zircon line
    row2_height = 1450  # Height for these blocks (needs to capture Marquis/Chinese Tee labels)

    page3_blocks_row2 = {
        21: (left_margin, row2_top, left_margin + col_width, row2_top + row2_height),
        22: (left_margin + col_width, row2_top, left_margin + 2*col_width, row2_top + row2_height),
    }

    for block_num, coords in page3_blocks_row2.items():
        cropped = page3.crop(coords)
        output_path = os.path.join(OUTPUT_DIR, f"FS-{block_num}.png")
        cropped.save(output_path, "PNG")
        print(f"Saved Block {block_num} to {output_path}")


def extract_random_formations(pages):
    """Extract random formations (A-Q)."""

    page4 = pages[3]

    # Randoms are in a 4x4 grid
    # Different layout - single formation per cell, not 3-part block
    header_offset = 380  # Below "Appendix D" header
    left_margin = 72
    col_width = 600
    row_height = 640  # Single formation height (reduced to avoid showing next row)

    randoms = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']

    for idx, letter in enumerate(randoms):
        col = idx % 4
        row = idx // 4

        left = left_margin + col * col_width
        top = header_offset + row * row_height
        right = left + col_width
        bottom = top + row_height

        cropped = page4.crop((left, top, right, bottom))
        output_path = os.path.join(OUTPUT_DIR, f"FS-{letter}.png")
        cropped.save(output_path, "PNG")
        print(f"Saved Random {letter} to {output_path}")


def extract_formations():
    """Extract formation images from the PDF."""

    print(f"Converting PDF to images at {DPI} DPI...")
    pages = convert_from_path(PDF_PATH, dpi=DPI)

    print(f"Found {len(pages)} pages\n")

    print("Extracting Block Sequences (1-22)...")
    extract_block_formations(pages)

    print("\nExtracting Random Formations (A-Q)...")
    extract_random_formations(pages)

    print("\nDone! All formations extracted to:", OUTPUT_DIR)


if __name__ == "__main__":
    extract_formations()
