#!/usr/bin/env bash
# tools/brandgen.sh - Deterministic Brand Asset Generator for Sydra OS
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOGO_SRC="$ROOT_DIR/assets/logo/sydra-logo.svg"
OUT_DIR="$ROOT_DIR/assets/logo/generated"

[[ -f "$LOGO_SRC" ]] || { echo "Error: $LOGO_SRC not found"; exit 1; }
mkdir -p "$OUT_DIR"

echo "=== Generating Sydra OS Brand Assets from $LOGO_SRC ==="

# 1. Generate Standard PNG sizes
for size in 16 24 32 48 64 128 256 512; do
    echo "  -> Generating ${size}x${size} PNG..."
    rsvg-convert -w "$size" -h "$size" "$LOGO_SRC" -o "$OUT_DIR/sydra-logo-${size}.png"
done

# 2. Simplified Favicon SVG (clean strokes, no outer glow for crisp small rendering)
cat << 'EOF' > "$OUT_DIR/sydra-logo-simplified.svg"
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="prism-grad-1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#5B8DEF" />
      <stop offset="100%" stop-color="#12141A" />
    </linearGradient>
    <linearGradient id="prism-grad-2" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#4FB3BF" />
      <stop offset="100%" stop-color="#1A1C24" />
    </linearGradient>
  </defs>
  <path d="M 256,48 L 440,154 L 440,366 L 256,472 L 72,366 L 72,154 Z"
        fill="#12141A" stroke="#5B8DEF" stroke-width="12" stroke-linejoin="round" />
  <path d="M 256,76 L 412,168 L 334,256 L 256,210 Z" fill="url(#prism-grad-1)" />
  <path d="M 256,444 L 100,352 L 178,256 L 256,302 Z" fill="url(#prism-grad-2)" />
  <path d="M 256,210 L 334,256 L 256,302 L 178,256 Z" fill="#FFFFFF" fill-opacity="0.35" />
</svg>
EOF

# Generate multi-resolution favicon.ico
rsvg-convert -w 16 -h 16 "$OUT_DIR/sydra-logo-simplified.svg" -o "$OUT_DIR/fav-16.png"
rsvg-convert -w 32 -h 32 "$OUT_DIR/sydra-logo-simplified.svg" -o "$OUT_DIR/fav-32.png"
rsvg-convert -w 48 -h 48 "$OUT_DIR/sydra-logo-simplified.svg" -o "$OUT_DIR/fav-48.png"
magick "$OUT_DIR/fav-16.png" "$OUT_DIR/fav-32.png" "$OUT_DIR/fav-48.png" "$OUT_DIR/favicon.ico"
rm -f "$OUT_DIR"/fav-*.png

# 3. Monochrome White & Dark SVGs
cat << 'EOF' > "$OUT_DIR/sydra-logo-mono-white.svg"
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <path d="M 256,48 L 440,154 L 440,366 L 256,472 L 72,366 L 72,154 Z"
        fill="none" stroke="#FFFFFF" stroke-width="14" stroke-linejoin="round" />
  <path d="M 256,76 L 412,168 L 334,256 L 256,210 Z" fill="#FFFFFF" fill-opacity="0.9" />
  <path d="M 256,444 L 100,352 L 178,256 L 256,302 Z" fill="#FFFFFF" fill-opacity="0.75" />
  <path d="M 256,210 L 334,256 L 256,302 L 178,256 Z" fill="#FFFFFF" fill-opacity="0.45" />
</svg>
EOF

cat << 'EOF' > "$OUT_DIR/sydra-logo-mono-dark.svg"
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <path d="M 256,48 L 440,154 L 440,366 L 256,472 L 72,366 L 72,154 Z"
        fill="none" stroke="#12141A" stroke-width="14" stroke-linejoin="round" />
  <path d="M 256,76 L 412,168 L 334,256 L 256,210 Z" fill="#12141A" fill-opacity="0.9" />
  <path d="M 256,444 L 100,352 L 178,256 L 256,302 Z" fill="#12141A" fill-opacity="0.75" />
  <path d="M 256,210 L 334,256 L 256,302 L 178,256 Z" fill="#12141A" fill-opacity="0.45" />
</svg>
EOF

# 4. Horizontal Lockup SVG & PNG
cat << 'EOF' > "$OUT_DIR/sydra-logo-lockup.svg"
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" width="800" height="200">
  <g transform="translate(30, 20) scale(0.3125)">
    <!-- Embed Outer Hexagon -->
    <path d="M 256,48 L 440,154 L 440,366 L 256,472 L 72,366 L 72,154 Z"
          fill="#12141A" fill-opacity="0.85" stroke="#FFFFFF" stroke-opacity="0.3" stroke-width="6" stroke-linejoin="round" />
    <path d="M 256,76 L 412,168 L 334,256 L 256,210 Z" fill="#5B8DEF" />
    <path d="M 256,444 L 100,352 L 178,256 L 256,302 Z" fill="#4FB3BF" />
    <path d="M 256,210 L 334,256 L 256,302 L 178,256 Z" fill="#FFFFFF" fill-opacity="0.3" />
  </g>
  <text x="220" y="125" font-family="Inter, sans-serif" font-size="72" font-weight="600" fill="#F2F4F8" letter-spacing="-1">Sydra<tspan fill="#5B8DEF" font-weight="300"> OS</tspan></text>
</svg>
EOF
rsvg-convert -w 800 -h 200 "$OUT_DIR/sydra-logo-lockup.svg" -o "$OUT_DIR/sydra-logo-lockup.png"

echo "=== Generated Assets in $OUT_DIR ==="
ls -lh "$OUT_DIR"
