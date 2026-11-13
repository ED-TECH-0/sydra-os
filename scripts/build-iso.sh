#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$PWD
WORK="$ROOT/build/work"
OUT="$ROOT/build/out"
LOGDIR="$ROOT/build/logs"
LOG="$LOGDIR/iso-$(date +%Y%m%d-%H%M%S).log"

[[ $EUID -eq 0 ]] || { echo "run with sudo (make iso does this)"; exit 1; }
mkdir -p "$OUT" "$LOGDIR"

avail_gb=$(df --output=avail -BG "$ROOT" | tail -1 | tr -dc '0-9')
(( avail_gb >= 25 )) || { echo "need >= 25 GB free, have ${avail_gb} GB"; exit 1; }

# render pacman.conf with absolute path to the local repo (after T2.2)
if [[ -f iso/profile/pacman.conf.in ]]; then
  sed "s|@REPO_DIR@|$ROOT|g" iso/profile/pacman.conf.in > iso/profile/pacman.conf
fi

rm -rf "$WORK"
mkarchiso -v -w "$WORK" -o "$OUT" iso/profile 2>&1 | tee "$LOG"

( cd "$OUT" && sha256sum ./*.iso > SHA256SUMS )
rm -rf "$WORK"
echo "ISO ready in $OUT"
