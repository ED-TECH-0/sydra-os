#!/usr/bin/env python3
"""
Sydra OS Procedural 4K Wallpaper Generator (Pure Python / SVG)
Generates dark, frosted glass wallpapers for Sydra Glass Pro.
Original procedural works (CC0 / Public Domain).
"""

import os
import sys

WALLPAPERS = [
    {
        "filename": "sydra-graphite-flow.svg",
        "title": "Sydra Graphite Flow",
        "bg_dark": "#0B0D12",
        "blobs": [
            {"cx": "30%", "cy": "40%", "r": "45%", "color": "#1A2E56", "opacity": "0.45"},
            {"cx": "75%", "cy": "60%", "r": "50%", "color": "#0E3E48", "opacity": "0.35"},
            {"cx": "50%", "cy": "85%", "r": "35%", "color": "#201D38", "opacity": "0.30"},
        ]
    },
    {
        "filename": "sydra-midnight-frost.svg",
        "title": "Sydra Midnight Frost",
        "bg_dark": "#07090E",
        "blobs": [
            {"cx": "20%", "cy": "25%", "r": "40%", "color": "#123048", "opacity": "0.40"},
            {"cx": "80%", "cy": "30%", "r": "45%", "color": "#1F2342", "opacity": "0.35"},
            {"cx": "60%", "cy": "75%", "r": "40%", "color": "#0D2A3A", "opacity": "0.35"},
        ]
    },
    {
        "filename": "sydra-slate-shadow.svg",
        "title": "Sydra Slate Shadow",
        "bg_dark": "#12141A",
        "blobs": [
            {"cx": "40%", "cy": "35%", "r": "55%", "color": "#222736", "opacity": "0.50"},
            {"cx": "70%", "cy": "70%", "r": "45%", "color": "#182030", "opacity": "0.40"},
        ]
    },
    {
        "filename": "sydra-obsidian-minimal.svg",
        "title": "Sydra Obsidian Minimal",
        "bg_dark": "#0A0B0E",
        "blobs": [
            {"cx": "50%", "cy": "50%", "r": "60%", "color": "#151821", "opacity": "0.35"},
        ]
    }
]

def generate_svg(wp, out_path):
    svg_header = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3840 2160" width="3840" height="2160">
  <defs>
    <filter id="ultra-blur" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="180" />
    </filter>
  </defs>

  <!-- Base Canvas -->
  <rect width="3840" height="2160" fill="{wp['bg_dark']}" />

  <!-- Luminous Blurred Ambient Blobs -->
  <g filter="url(#ultra-blur)">
"""
    blobs_svg = ""
    for b in wp['blobs']:
        blobs_svg += f'    <circle cx="{b["cx"]}" cy="{b["cy"]}" r="{b["r"]}" fill="{b["color"]}" fill-opacity="{b["opacity"]}" />\n'

    svg_footer = """  </g>

  <!-- Subtle Film Grain / Vignette Overlay -->
  <radialGradient id="vignette" cx="50%" cy="50%" r="70%">
    <stop offset="60%" stop-color="#000000" stop-opacity="0.0" />
    <stop offset="100%" stop-color="#000000" stop-opacity="0.45" />
  </radialGradient>
  <rect width="3840" height="2160" fill="url(#vignette)" />
</svg>
"""
    with open(out_path, "w") as f:
        f.write(svg_header + blobs_svg + svg_footer)
    print(f"Generated {out_path} ({wp['title']})")

def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "assets/wallpapers"
    os.makedirs(out_dir, exist_ok=True)
    for wp in WALLPAPERS:
        target = os.path.join(out_dir, wp["filename"])
        generate_svg(wp, target)
    print("All wallpapers generated successfully.")

if __name__ == "__main__":
    main()
