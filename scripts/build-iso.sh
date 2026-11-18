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

# render pacman.conf with URL-encoded path for pacman file:// compatibility
if [[ -f iso/profile/pacman.conf.in ]]; then
  REPO_ENC=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$ROOT'''))")
  sed "s|@REPO_DIR@|$REPO_ENC|g" iso/profile/pacman.conf.in > iso/profile/pacman.conf
fi

# Safely unmount any lingering mounts from previous aborted runs
for mnt in "$WORK/x86_64/airootfs/proc" "$WORK/x86_64/airootfs/sys" "$WORK/x86_64/airootfs/dev" "$WORK/x86_64/airootfs/run"; do
  if [ -d "$mnt" ] && mountpoint -q "$mnt" 2>/dev/null; then
    umount -l "$mnt" 2>/dev/null || true
  fi
done
(grep -F "$WORK" /proc/mounts 2>/dev/null || true) | awk '{print $2}' | sort -r | while read -r m; do
  [[ -n "$m" ]] && umount -l "$m" 2>/dev/null || true
done

rm -rf "$WORK"
echo "Starting mkarchiso build..."
mkarchiso -v -w "$WORK" -o "$OUT" iso/profile 2>&1 | tee "$LOG"

( cd "$OUT" && sha256sum ./*.iso > SHA256SUMS )

# Safely unmount before deleting work
(grep -F "$WORK" /proc/mounts 2>/dev/null || true) | awk '{print $2}' | sort -r | while read -r m; do
  [[ -n "$m" ]] && umount -l "$m" 2>/dev/null || true
done
rm -rf "$WORK"
echo "ISO ready in $OUT"
