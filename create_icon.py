#!/usr/bin/env python3
"""
Create an app icon for Draw Generator.
Creates a simple icon with skydivers/formation imagery.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a 1024x1024 icon (required for macOS)
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background - dark blue gradient-like circle
    center = size // 2
    radius = size // 2 - 20

    # Draw background circle
    draw.ellipse([center - radius, center - radius, center + radius, center + radius],
                 fill='#1e3a5f')

    # Draw inner circle (lighter)
    inner_radius = radius - 40
    draw.ellipse([center - inner_radius, center - inner_radius,
                  center + inner_radius, center + inner_radius],
                 fill='#2563eb')

    # Draw 4 stylized skydivers in a star formation
    skydiver_color = 'white'
    skydiver_size = 120

    # Positions for 4-way star
    positions = [
        (center, center - 200),  # Top
        (center + 200, center),  # Right
        (center, center + 200),  # Bottom
        (center - 200, center),  # Left
    ]

    for x, y in positions:
        # Draw simple skydiver shape (circle head + body)
        head_r = 35
        draw.ellipse([x - head_r, y - head_r - 30, x + head_r, y + head_r - 30],
                     fill=skydiver_color)
        # Body
        draw.ellipse([x - 50, y - 10, x + 50, y + 70], fill=skydiver_color)
        # Arms (rectangles extending out)
        draw.rectangle([x - 100, y + 10, x - 40, y + 40], fill=skydiver_color)
        draw.rectangle([x + 40, y + 10, x + 100, y + 40], fill=skydiver_color)
        # Legs
        draw.rectangle([x - 40, y + 60, x - 10, y + 130], fill=skydiver_color)
        draw.rectangle([x + 10, y + 60, x + 40, y + 130], fill=skydiver_color)

    # Draw center connection (star point)
    draw.ellipse([center - 60, center - 60, center + 60, center + 60],
                 fill='#fbbf24')

    # Add text "DG" in center
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
    except:
        font = ImageFont.load_default()

    draw.text((center, center), "DG", fill='#1e3a5f', font=font, anchor='mm')

    # Save as PNG first
    png_path = '/Users/kevindrivas/Desktop/projects/draw-generator/icon.png'
    img.save(png_path, 'PNG')
    print(f"Saved PNG icon: {png_path}")

    # Create iconset directory for macOS .icns
    iconset_path = '/Users/kevindrivas/Desktop/projects/draw-generator/DrawGenerator.iconset'
    os.makedirs(iconset_path, exist_ok=True)

    # Generate required sizes for macOS iconset
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(os.path.join(iconset_path, f'icon_{s}x{s}.png'), 'PNG')
        if s <= 512:
            # Also save @2x versions
            resized_2x = img.resize((s * 2, s * 2), Image.Resampling.LANCZOS)
            resized_2x.save(os.path.join(iconset_path, f'icon_{s}x{s}@2x.png'), 'PNG')

    print(f"Created iconset at: {iconset_path}")
    print("Run: iconutil -c icns DrawGenerator.iconset")

    return png_path

if __name__ == '__main__':
    create_icon()
