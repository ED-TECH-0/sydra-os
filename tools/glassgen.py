#!/usr/bin/env python3
"""
Siddha Glass Pro / Sydra OS Design Token Compiler & Theme Generator
Generates KDE color schemes, Kvantum configurations, SDDM variables,
Konsole profiles, and GTK CSS from tokens/glass.json.
"""

import sys
import os
import json
import argparse
import math

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

def srgb_to_linear(c):
    c = c / 255.0
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4

def relative_luminance(rgb):
    r_lin = srgb_to_linear(rgb[0])
    g_lin = srgb_to_linear(rgb[1])
    b_lin = srgb_to_linear(rgb[2])
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

def blend_colors(fg_rgb, fg_alpha, bg_rgb):
    return tuple(fg_rgb[i] * fg_alpha + bg_rgb[i] * (1.0 - fg_alpha) for i in range(3))

def contrast_ratio(rgb1, rgb2):
    lum1 = relative_luminance(rgb1)
    lum2 = relative_luminance(rgb2)
    l_bright = max(lum1, lum2)
    l_dark = min(lum1, lum2)
    return (l_bright + 0.05) / (l_dark + 0.05)

def validate_tokens(tokens):
    print("=== Validating tokens/glass.json ===")
    errors = []
    
    # 1. Structure check
    for key in ['version', 'name', 'radius', 'blur', 'opacity', 'border', 'shadow', 'presets']:
        if key not in tokens:
            errors.append(f"Missing required key in tokens: '{key}'")
            
    # 2. Presets check & contrast validation
    presets = tokens.get('presets', {})
    min_contrast = tokens.get('contrast', {}).get('minTextRatio', 4.5)
    
    test_backdrops = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'dark-wallpaper': (26, 26, 36),
        'bright-wallpaper': (224, 229, 236),
        'vivid-gradient': (90, 40, 180)
    }
    
    print(f"Checking contrast against {len(test_backdrops)} reference backgrounds (target >= {min_contrast}:1):")
    
    for preset_name, preset in presets.items():
        tint_rgb = hex_to_rgb(preset['tint'])
        text_rgb = hex_to_rgb(preset['text'])
        accent_rgb = hex_to_rgb(preset['accent'])
        opacity = tokens.get('opacity', {}).get('window', 0.80)
        
        print(f"\n Preset: [{preset_name}]")
        print(f"   Tint: {preset['tint']} (alpha: {opacity}), Text: {preset['text']}, Accent: {preset['accent']}")
        
        for bg_name, bg_rgb in test_backdrops.items():
            surface_rgb = blend_colors(tint_rgb, opacity, bg_rgb)
            ratio = contrast_ratio(text_rgb, surface_rgb)
            status = "PASS" if ratio >= min_contrast else "FAIL"
            print(f"   - over {bg_name:<16}: ratio {ratio:.2f}:1 -> [{status}]")
            if ratio < min_contrast:
                errors.append(f"Preset '{preset_name}' fails contrast over '{bg_name}': {ratio:.2f}:1 < {min_contrast}:1")
                
    if errors:
        print("\nValidation FAILED:")
        for err in errors:
            print(f"  [ERROR] {err}")
        return False
        
    print("\nAll token and contrast checks PASSED!")
    return True

def generate_kde_colorscheme(tokens, preset_name, out_path):
    preset = tokens['presets'][preset_name]
    tint_rgb = hex_to_rgb(preset['tint'])
    text_rgb = hex_to_rgb(preset['text'])
    muted_rgb = hex_to_rgb(preset['muted'])
    accent_rgb = hex_to_rgb(preset['accent'])
    
    tint_str = f"{tint_rgb[0]},{tint_rgb[1]},{tint_rgb[2]}"
    text_str = f"{text_rgb[0]},{text_rgb[1]},{text_rgb[2]}"
    muted_str = f"{muted_rgb[0]},{muted_rgb[1]},{muted_rgb[2]}"
    accent_str = f"{accent_rgb[0]},{accent_rgb[1]},{accent_rgb[2]}"
    
    content = f"""[General]
ColorScheme=SiddhaGlass-{preset_name.capitalize()}
Name=Siddha Glass ({preset_name.capitalize()})
shadeSortColumn=true

[Colors:Window]
BackgroundNormal={tint_str}
BackgroundAlternate={tint_str}
ForegroundNormal={text_str}
ForegroundInactive={muted_str}
ForegroundActive={accent_str}
ForegroundLink={accent_str}

[Colors:View]
BackgroundNormal={tint_str}
BackgroundAlternate={tint_str}
ForegroundNormal={text_str}
ForegroundInactive={muted_str}
ForegroundLink={accent_str}

[Colors:Button]
BackgroundNormal={tint_str}
ForegroundNormal={text_str}
ForegroundActive={accent_str}

[Colors:Selection]
BackgroundNormal={accent_str}
ForegroundNormal=255,255,255

[Colors:Tooltip]
BackgroundNormal={tint_str}
ForegroundNormal={text_str}

[WM]
activeBackground={tint_str}
activeForeground={text_str}
inactiveBackground={tint_str}
inactiveForeground={muted_str}
"""
    with open(out_path, 'w') as f:
        f.write(content)

def generate_konsole_profile(tokens, preset_name, out_dir):
    preset = tokens['presets'][preset_name]
    text_rgb = hex_to_rgb(preset['text'])
    tint_rgb = hex_to_rgb(preset['tint'])
    accent_rgb = hex_to_rgb(preset['accent'])
    opacity = tokens.get('opacity', {}).get('terminal', 0.88)
    
    os.makedirs(out_dir, exist_ok=True)
    cs_path = os.path.join(out_dir, f"SiddhaGlass{preset_name.capitalize()}.colorscheme")
    
    cs_content = f"""[General]
Description=Siddha Glass {preset_name.capitalize()}
Opacity={opacity}
Blur=true
Wallpaper=

[Background]
Color={tint_rgb[0]},{tint_rgb[1]},{tint_rgb[2]}

[Foreground]
Color={text_rgb[0]},{text_rgb[1]},{text_rgb[2]}

[Color0]
Color=0,0,0

[Color1]
Color=235,95,95

[Color2]
Color=95,215,95

[Color3]
Color=240,200,95

[Color4]
Color={accent_rgb[0]},{accent_rgb[1]},{accent_rgb[2]}

[Color5]
Color=180,120,240

[Color6]
Color=95,215,215

[Color7]
Color=240,240,240
"""
    with open(cs_path, 'w') as f:
        f.write(cs_content)

def generate_cosmic_theme(tokens, preset_name, out_dir):
    preset = tokens['presets'][preset_name]
    tint_rgb = hex_to_rgb(preset['tint'])
    accent_rgb = hex_to_rgb(preset['accent'])
    
    r_tint, g_tint, b_tint = [round(c / 255.0, 3) for c in tint_rgb]
    r_acc, g_acc, b_acc = [round(c / 255.0, 3) for c in accent_rgb]
    
    cosmic_builder_dir = os.path.join(out_dir, f"cosmic-{preset_name}", "com.system76.CosmicTheme.Dark.Builder", "v2")
    os.makedirs(cosmic_builder_dir, exist_ok=True)
    
    with open(os.path.join(cosmic_builder_dir, "frosted"), "w") as f:
        f.write("ExtremelyLow\n")
    with open(os.path.join(cosmic_builder_dir, "frosted_windows"), "w") as f:
        f.write("true\n")
    with open(os.path.join(cosmic_builder_dir, "frosted_panel"), "w") as f:
        f.write("true\n")
    with open(os.path.join(cosmic_builder_dir, "frosted_applets"), "w") as f:
        f.write("true\n")
    with open(os.path.join(cosmic_builder_dir, "frosted_system_interface"), "w") as f:
        f.write("true\n")
    with open(os.path.join(cosmic_builder_dir, "interface_density"), "w") as f:
        f.write("Comfortable\n")
    with open(os.path.join(cosmic_builder_dir, "accent"), "w") as f:
        f.write(f"Some(({r_acc}, {g_acc}, {b_acc}))\n")
    with open(os.path.join(cosmic_builder_dir, "bg_color"), "w") as f:
        f.write(f"({r_tint}, {g_tint}, {b_tint})\n")
    with open(os.path.join(cosmic_builder_dir, "alpha_map"), "w") as f:
        f.write("""(
    extremely_low: 0.35,
    extremely_low_2: 0.38,
    very_low: 0.42,
    very_low_2: 0.46,
    low: 0.50,
    low_2: 0.55,
    medium: 0.60,
    medium_2: 0.65,
    high: 0.70,
    high_2: 0.75,
    very_high: 0.80,
    very_high_2: 0.85,
    extremely_high: 0.88,
    extremely_high_2: 0.92,
)
""")
    with open(os.path.join(cosmic_builder_dir, "corner_radii"), "w") as f:
        f.write("""(
    radius_0: (0.0, 0.0, 0.0, 0.0),
    radius_xs: (4.0, 4.0, 4.0, 4.0),
    radius_s: (8.0, 8.0, 8.0, 8.0),
    radius_m: (14.0, 14.0, 14.0, 14.0),
    radius_l: (24.0, 24.0, 24.0, 24.0),
    radius_xl: (160.0, 160.0, 160.0, 160.0),
)
""")
    with open(os.path.join(cosmic_builder_dir, "gaps"), "w") as f:
        f.write("(8, 8)\n")

    # Cosmic terminal profile
    term_dir = os.path.join(out_dir, f"cosmic-{preset_name}", "com.system76.CosmicTerm", "v1")
    os.makedirs(term_dir, exist_ok=True)
    with open(os.path.join(term_dir, "font_name"), "w") as f:
        f.write(f'"{tokens["fonts"]["mono"]}"\n')
    with open(os.path.join(term_dir, "opacity"), "w") as f:
        f.write(f"{tokens['opacity']['terminal']}\n")

def generate_gtk_css(tokens, preset_name, out_path):
    preset = tokens['presets'][preset_name]
    tint_rgb = hex_to_rgb(preset['tint'])
    text_rgb = hex_to_rgb(preset['text'])
    accent_rgb = hex_to_rgb(preset['accent'])
    
    opacity = tokens.get('opacity', {}).get('window', 0.80)
    radius = tokens.get('radius', {}).get('window', 12)
    
    content = f"""/* Sydra OS / Siddha Glass GTK Overrides - Preset: {preset_name} */
@define-color accent_color {preset['accent']};
@define-color window_bg_color rgba({tint_rgb[0]}, {tint_rgb[1]}, {tint_rgb[2]}, {opacity});
@define-color window_fg_color {preset['text']};

window {{
    background-color: @window_bg_color;
    color: @window_fg_color;
    border-radius: {radius}px;
}}

headerbar {{
    background-color: rgba({tint_rgb[0]}, {tint_rgb[1]}, {tint_rgb[2]}, 0.90);
    border-bottom: 1px solid rgba(255, 255, 255, 0.10);
}}

button {{
    border-radius: {tokens['radius']['control']}px;
}}
"""
    with open(out_path, 'w') as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description="Siddha Glass Token Compiler")
    parser.add_argument("--tokens", default="tokens/glass.json", help="Path to tokens.json")
    parser.add_argument("--check", action="store_true", help="Validate tokens and contrast ratios")
    parser.add_argument("--out-dir", default="build/theme", help="Output directory for generated themes")
    args = parser.parse_args()
    
    if not os.path.exists(args.tokens):
        print(f"Error: {args.tokens} not found", file=sys.stderr)
        sys.exit(1)
        
    with open(args.tokens) as f:
        tokens = json.load(f)
        
    if args.check:
        valid = validate_tokens(tokens)
        sys.exit(0 if valid else 1)
        
    os.makedirs(args.out_dir, exist_ok=True)
    print(f"Compiling themes to {args.out_dir}...")
    
    for preset in tokens['presets']:
        generate_cosmic_theme(tokens, preset, args.out_dir)

        kde_out = os.path.join(args.out_dir, f"SiddhaGlass{preset.capitalize()}.colors")
        generate_kde_colorscheme(tokens, preset, kde_out)
        
        konsole_dir = os.path.join(args.out_dir, "konsole")
        generate_konsole_profile(tokens, preset, konsole_dir)
        
        gtk_out = os.path.join(args.out_dir, f"gtk-{preset}.css")
        generate_gtk_css(tokens, preset, gtk_out)
        
    print("Theme generation complete.")

if __name__ == "__main__":
    main()
