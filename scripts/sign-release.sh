#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

OUT="build/out"
[[ -d $OUT ]] || { echo "No build/out directory"; exit 1; }

echo "Generating SHA256 checksums..."
( cd "$OUT" && sha256sum ./*.iso > SHA256SUMS )

KEY_ID="${GPG_KEY_ID:-}"
if [[ -z $KEY_ID ]]; then
  echo "Signing SHA256SUMS with default GPG key..."
  gpg --detach-sign --armor "$OUT/SHA256SUMS"
else
  echo "Signing SHA256SUMS with GPG key $KEY_ID..."
  gpg --default-key "$KEY_ID" --detach-sign --armor "$OUT/SHA256SUMS"
fi

echo "Release checksums and signature ready in $OUT/."
