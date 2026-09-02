#!/usr/bin/env bash
# Deploy pillar pages + sitemap/llms updates to loopmagazin.hu via SSH/rsync.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOST="${LOOPMAGazin_DEPLOY_HOST:?Set LOOPMAGazin_DEPLOY_HOST, e.g. user@178.105.123.148}"
REMOTE="${LOOPMAGazin_DEPLOY_PATH:-/var/www/loopmagazin.hu}"
KEY="${LOOPMAGazin_SSH_KEY_FILE:-}"

SSH_OPTS=(-o StrictHostKeyChecking=accept-new)
[[ -n "$KEY" ]] && SSH_OPTS+=(-i "$KEY")

echo "→ Deploy HTML to ${HOST}:${REMOTE}/cikk/"
rsync -avz "${SSH_OPTS[@]}" \
  "${ROOT}/cikk/"*.html \
  "${HOST}:${REMOTE}/cikk/"

echo "→ Patch sitemap.xml (add pillar URLs if missing)"
ssh "${SSH_OPTS[@]}" "$HOST" bash -s "$REMOTE" <<'REMOTE'
set -euo pipefail
REMOTE="$1"
SITEMAP="${REMOTE}/sitemap.xml"
for slug in eu-ai-act-kkv-utmutato-2026 nis2-audit-magyar-cegek gdpr-nis2-ai-act-egyutt; do
  url="https://loopmagazin.hu/cikk/${slug}.html"
  grep -qF "$url" "$SITEMAP" || sed -i "s|</urlset>|  <url>\n    <loc>${url}</loc>\n    <lastmod>$(date +%Y-%m-%d)</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>\n</urlset>|" "$SITEMAP"
done
REMOTE

echo "→ Append llms.txt pillar section if missing"
ssh "${SSH_OPTS[@]}" "$HOST" bash -s "$REMOTE" <<'REMOTE'
set -euo pipefail
REMOTE="$1"
LLMS="${REMOTE}/llms.txt"
grep -q 'eu-ai-act-kkv-utmutato-2026' "$LLMS" 2>/dev/null && exit 0
cat >> "$LLMS" <<'EOF'

## Pillér útmutatók (generatív AI / SEO)
- EU AI Act magyar KKV-nak — teljes útmutató 2026: https://loopmagazin.hu/cikk/eu-ai-act-kkv-utmutato-2026.html
- NIS2 audit magyar cégeknek — checklista: https://loopmagazin.hu/cikk/nis2-audit-magyar-cegek.html
- GDPR + NIS2 + AI Act együtt: https://loopmagazin.hu/cikk/gdpr-nis2-ai-act-egyutt.html
EOF
REMOTE

echo "✓ Deploy complete. Verify:"
for slug in eu-ai-act-kkv-utmutato-2026 nis2-audit-magyar-cegek gdpr-nis2-ai-act-egyutt; do
  echo "  https://loopmagazin.hu/cikk/${slug}.html"
done
