#!/usr/bin/env bash
# Stage the playable game in dist/ and publish it on Vercel.
#   ./deploy.sh           stage dist/ only (serve it with python3 -m http.server -d dist)
#   ./deploy.sh --prod    stage, then deploy dist/ to production on Vercel
# Three.js is served from the site itself rather than jsDelivr, so a shared link
# depends on one host only. SITE is the public address the X card points at.
set -euo pipefail
cd "$(dirname "$0")"
SITE="${SITE:-https://dockstack.vercel.app}"
THREE_VERSION=0.170.0

# Keep Vercel's project link (dist/.vercel) between builds.
mkdir -p dist
find dist -mindepth 1 -maxdepth 1 ! -name .vercel -exec rm -rf {} +
cp -R index.html sim.js icon.svg og.jpg CREDITS.md assets dist/

# Vendor the Three.js files the page imports, plus everything they import in turn.
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
(cd "$tmp" && npm pack --silent "three@$THREE_VERSION" > /dev/null && tar -xzf three-*.tgz)
node --input-type=module - "$tmp/package" dist/vendor/three <<'EOF'
import { readFileSync, mkdirSync, copyFileSync } from 'node:fs';
import { dirname, join, normalize } from 'node:path';
const [src, out] = process.argv.slice(2);
const html = readFileSync('index.html', 'utf8');
const queue = ['build/three.module.min.js',
  ...[...html.matchAll(/from 'three\/addons\/([^']+)'/g)].map((m) => `examples/jsm/${m[1]}`)];
const seen = new Set();
while (queue.length) {
  const file = queue.pop();
  if (seen.has(file)) continue;
  seen.add(file);
  const text = readFileSync(join(src, file), 'utf8');
  for (const m of text.matchAll(/(?:from|import)\s*['"](\.{1,2}\/[^'"]+)['"]/g)) queue.push(normalize(join(dirname(file), m[1])));
  mkdirSync(join(out, dirname(file)), { recursive: true });
  copyFileSync(join(src, file), join(out, file));
}
console.log(`vendored ${seen.size} Three.js files`);
EOF
cp "$tmp/package/LICENSE" dist/vendor/three/LICENSE

# Point the import map at the vendored copy, preload every module to avoid a
# request waterfall, and add the tags X and other sites read for the link card.
node --input-type=module - "$SITE" <<'EOF'
import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
const site = process.argv[2].replace(/\/$/, '');
let html = readFileSync('dist/index.html', 'utf8');
const cdn = 'https://cdn.jsdelivr.net/npm/three@0.170.0/';
if (!html.includes(cdn)) throw new Error('import map no longer points at jsDelivr three@0.170.0');
html = html.replaceAll(cdn, './vendor/three/');
const walk = (d) => readdirSync(d).flatMap((f) => statSync(join(d, f)).isDirectory() ? walk(join(d, f)) : [join(d, f)]);
const preloads = walk('dist/vendor/three').filter((f) => f.endsWith('.js'))
  .map((f) => `<link rel="modulepreload" href="${f.replace(/^dist\//, './')}">`).join('\n');
const card = `
<meta property="og:type" content="website">
<meta property="og:url" content="${site}/">
<meta property="og:title" content="Dockstack">
<meta property="og:description" content="Drop crates from a harbour crane onto a rocking boat. A new shipment every day, the same for everyone.">
<meta property="og:image" content="${site}/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A harbour crane lowering a crate onto a stack of crates on a boat at sunset">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Dockstack">
<meta name="twitter:description" content="Drop crates from a harbour crane onto a rocking boat. A new shipment every day.">
<meta name="twitter:image" content="${site}/og.jpg">
<meta name="twitter:image:alt" content="A harbour crane lowering a crate onto a stack of crates on a boat at sunset">
<link rel="canonical" href="${site}/">
`;
html = html.replace('</head>', `${card}${preloads}\n</head>`);
writeFileSync('dist/index.html', html);
EOF
du -sh dist | cut -f1 | xargs printf 'dist/ staged: %s\n'

if [[ "${1:-}" == "--prod" ]]; then
  vercel deploy dist --prod --yes
fi
