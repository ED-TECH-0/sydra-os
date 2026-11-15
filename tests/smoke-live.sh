#!/usr/bin/env bash
set -euo pipefail

echo "=============================================="
echo "          Sydra OS Live Smoke Test"
echo "=============================================="

FAILURES=0
pass() { echo "[PASS] $1"; }
fail() { echo "[FAIL] $1"; FAILURES=$((FAILURES + 1)); }

# 1. Kernel check
KERNEL=$(uname -r)
pass "Kernel running: $KERNEL"

# 2. Session check
if [[ "${XDG_SESSION_TYPE:-}" == "wayland" ]]; then
  pass "Wayland session active ($XDG_SESSION_TYPE)"
else
  echo "[INFO] Session type: ${XDG_SESSION_TYPE:-unset}"
fi

# 3. Systemd units check
FAILED_UNITS=$(systemctl --failed --no-legend 2>/dev/null || true)
if [[ -z $FAILED_UNITS ]]; then
  pass "No failed systemd units"
else
  fail "Failed systemd units found:"
  echo "$FAILED_UNITS"
fi

# 4. Audio check
if command -v pactl &>/dev/null && pactl info &>/dev/null; then
  pass "PipeWire / Pulse audio server responsive"
else
  fail "Audio server not responsive or pactl missing"
fi

# 5. NetworkManager check
if systemctl is-active --quiet NetworkManager; then
  pass "NetworkManager active"
else
  fail "NetworkManager not active"
fi

# 6. Core utilities check
for cmd in steam zsh git dolphin konsole; do
  if command -v "$cmd" &>/dev/null; then
    pass "Core binary present: $cmd"
  else
    fail "Core binary missing: $cmd"
  fi
done

# 7. Custom Sydra OS utilities check
for scmd in siddha-dev siddha-gpu-setup siddha-gamehub siddha-glass-set siddha-welcome siddha-update siddha-rollback siddha-installer calamares; do
  if command -v "$scmd" &>/dev/null; then
    pass "Sydra binary present: $scmd"
  else
    fail "Sydra binary missing: $scmd"
  fi
done

# 8. Glassmorphism assets check
if [ -d "/usr/share/plasma/look-and-feel/org.sydra.glass.desktop" ]; then
  pass "Look-and-feel present: org.sydra.glass.desktop"
else
  fail "Look-and-feel missing: org.sydra.glass.desktop"
fi

if [ -f "/usr/share/wallpapers/Sydra/contents/images/3840x2160.png" ] || [ -f "/usr/share/wallpapers/Sydra/sydra-obsidian-waves.png" ]; then
  pass "Wallpaper present: sydra-obsidian-waves.png"
else
  fail "Wallpaper missing: sydra-obsidian-waves.png"
fi

if [ -f "/usr/share/color-schemes/SiddhaGlassGraphite.colors" ]; then
  pass "Color scheme present: SiddhaGlassGraphite.colors"
else
  fail "Color scheme missing: SiddhaGlassGraphite.colors"
fi

echo "=============================================="
if (( FAILURES == 0 )); then
  echo "All live smoke tests passed successfully with 0 failures!"
  exit 0
else
  echo "$FAILURES test(s) failed."
  exit 1
fi
