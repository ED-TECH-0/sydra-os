#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

ISO_PATH=${1:-}
if [[ -z $ISO_PATH ]]; then
  ISO_PATH=$(ls -1t build/out/sydra-os-*.iso 2>/dev/null | head -n1 || true)
fi

[[ -n $ISO_PATH && -f $ISO_PATH ]] || { echo "ISO file not found: ${ISO_PATH:-none}"; exit 1; }

# Locate Ventoy mount
VENTOY_DIR=$(find /run/media /media /mnt -maxdepth 3 -type d -name "Ventoy" 2>/dev/null | head -n1 || true)

if [[ -z $VENTOY_DIR ]]; then
  echo "Error: Ventoy partition not found mounted under /run/media, /media, or /mnt."
  echo "Mount your Ventoy pendrive first."
  exit 1
fi

echo "Found Ventoy partition at: $VENTOY_DIR"
echo "Copying $(basename "$ISO_PATH")..."
cp --progress=bar "$ISO_PATH" "$VENTOY_DIR/"

if [[ -f build/out/SHA256SUMS ]]; then
  cp build/out/SHA256SUMS "$VENTOY_DIR/"
fi

sync
echo "Copy complete and synced."
