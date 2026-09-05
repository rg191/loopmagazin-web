#!/usr/bin/env bash
# Upload SEO-fixed article HTML to loopmagazin.hu (Mac-ről, ahol SSH működik).
set -euo pipefail

FIX_DIR="${1:-$(cd "$(dirname "$0")/../../loopmagazin-fix/cikk" && pwd)}"
HOST="${LOOPMAGazin_DEPLOY_HOST:?export LOOPMAGazin_DEPLOY_HOST=user@178.105.123.148}"
REMOTE="${LOOPMAGazin_DEPLOY_PATH:-/var/www/loopmagazin.hu}"
KEY="${LOOPMAGazin_SSH_KEY_FILE:-$HOME/.ssh/id_ed25519}"

echo "→ ${FIX_DIR} → ${HOST}:${REMOTE}/cikk/ (${KEY})"
rsync -avz -e "ssh -i ${KEY} -o StrictHostKeyChecking=accept-new" \
  "${FIX_DIR}/" \
  "${HOST}:${REMOTE}/cikk/"

echo "✓ Feltöltve. Ellenőrizd pl.:"
echo "  curl -sI https://loopmagazin.hu/cikk/uzleti-titok-ai-korban.html | grep last-modified"
