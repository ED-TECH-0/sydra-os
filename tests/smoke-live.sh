#!/usr/bin/env bash
set -euo pipefail

echo "=== Sydra OS Live Smoke Test ==="

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

# 5. NetworkManager
if systemctl is-active --quiet NetworkManager; then
  pass "NetworkManager active"
else
  fail "NetworkManager not active"
fi

# 6. Core utilities check
for cmd in steam zsh git dolphin konsole; do
  if command -v "$cmd" &>/dev/null; then
    pass "Binary present: $cmd"
  else
    fail "Binary missing: $cmd"
  fi
done

echo "================================"
if (( FAILURES == 0 )); then
  echo "All live smoke tests passed!"
  exit 0
else
  echo "$FAILURES tests failed."
  exit 1
fi
