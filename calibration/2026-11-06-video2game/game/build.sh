#!/usr/bin/env bash
# Build the game's compressed models from their sources, then validate them:
# the dock set from ../blender/out (written by blender/export.py) and the crate
# kit from calibration/2026-11-06-kit. Meshopt cuts the models by about 65%;
# the page loads them through Three.js's MeshoptDecoder.
set -euo pipefail
cd "$(dirname "$0")"
gt() { npx -y @gltf-transform/cli@4.5.1 "$@"; }
mkdir -p assets/models/kit
for f in ../blender/out/*.glb; do
  gt meshopt "$f" "assets/models/$(basename "$f")" > /dev/null
done
for n in crate_01 crate_half_01 crate_long_01 lid_box_01 plank_stack_01 pallet_01; do
  gt meshopt "../../2026-11-06-kit/$n.glb" "assets/models/kit/$n.glb" > /dev/null
done
for f in assets/models/*.glb assets/models/kit/*.glb; do
  out=$(gt validate "$f" 2>&1)
  grep -q "No errors found" <<< "$out" || { echo "invalid: $f"; echo "$out"; exit 1; }
  printf '%-36s %4s KB, valid\n' "$f" "$(du -k "$f" | cut -f1)"
done
