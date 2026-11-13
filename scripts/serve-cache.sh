#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-8080}
CACHE_DIR="/var/cache/pacman/pkg"

[[ -d $CACHE_DIR ]] || { echo "Cache dir not found: $CACHE_DIR"; exit 1; }

IP=$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{print $7}' | tr -d ' ' || echo "127.0.0.1")

echo "=================================================="
echo "Serving pacman cache over HTTP on port $PORT"
echo "URL: http://$IP:$PORT"
echo "WARNING: Accessible to devices on the local network."
echo "Press Ctrl+C to stop."
echo "=================================================="

exec python -m http.server "$PORT" --directory "$CACHE_DIR"
