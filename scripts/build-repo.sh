#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
ROOT=$PWD
REPO_DIR="$ROOT/repo/x86_64"
PKGBUILD_DIR="$ROOT/repo/pkgbuilds"
CHROOT_DIR="${CHROOT_DIR:-$HOME/chroot}"
LOGDIR="$ROOT/build/logs"

mkdir -p "$REPO_DIR" "$LOGDIR"

ORDER_FILE="$ROOT/repo/build-order.txt"
if [[ ! -f $ORDER_FILE ]]; then
  echo "No repo/build-order.txt found. Nothing to build."
  exit 0
fi

echo "Building custom packages in clean chroot ($CHROOT_DIR)..."

while IFS= read -r pkg || [[ -n $pkg ]]; do
  [[ -z $pkg || $pkg =~ ^# ]] && continue
  
  PKG_DIR="$PKGBUILD_DIR/$pkg"
  [[ -d $PKG_DIR ]] || { echo "Package directory not found: $PKG_DIR"; exit 1; }
  
  echo "=== Building $pkg ==="
  LOG="$LOGDIR/build-$pkg-$(date +%Y%m%d-%H%M%S).log"
  
  (
    cd "$PKG_DIR"
    # Find existing local packages to inject as dependencies
    INJECT_ARGS=()
    for local_pkg in "$REPO_DIR"/*.pkg.tar.zst; do
      if [[ -f $local_pkg ]]; then
        INJECT_ARGS+=("-I" "$local_pkg")
      fi
    done

    makechrootpkg -c -r "$CHROOT_DIR" "${INJECT_ARGS[@]}" 2>&1 | tee "$LOG"
    mv ./*.pkg.tar.zst "$REPO_DIR/"
  )

  repo-add "$REPO_DIR/siddha.db.tar.zst" "$REPO_DIR"/*.pkg.tar.zst
  echo "Package $pkg built and added to [siddha] repo."
done < "$ORDER_FILE"

echo "Repository build complete."
