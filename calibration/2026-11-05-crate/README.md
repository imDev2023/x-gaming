# Calibration 1: Crate_01, brief to Three.js

Run on 2026-11-05 for [issue #2](https://github.com/imDev2023/x-gaming/issues/2), following the Blender asset loop in [WORKFLOW.md](../../WORKFLOW.md).
No paid calls were made.

## What ran

- **Bridge: not used yet.**
  Installing MCP for Blender (adding it to Claude Code and copying its add-on into Blender) was stopped by Claude Code's permission check and needs the owner's approval.
  This run drove Blender headless with our own script instead, the way Atlas's `model3d-gen` does, so the loop itself could be tested now.
- **Brief:** [brief.md](brief.md), filled in from the workflow's template.
- **Build, checks, look renders and export:** [build_crate.py](build_crate.py), run with Blender 4.3.0:

  ```bash
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
    --python calibration/2026-11-05-crate/build_crate.py -- calibration/2026-11-05-crate
  ```

- **Validation:** `npx @gltf-transform/cli@4.5.1 validate crate_01.glb` and `inspect`.
- **Engine check:** [viewer.html](viewer.html), served locally, loads the GLB in Three.js 0.170 next to a 1.8 m stand-in player and a 1 m grid, and reports what the engine measured.

## Result

Every done check passes on the third build.

| Check | Result |
| --- | --- |
| Bounds | 1.000 x 1.000 x 1.000 m in Blender and in Three.js |
| Triangles | 300 of a 500 budget |
| Origin | bottom center; minimum Y is 0 and X, Z are centered in the engine |
| Transforms | applied |
| Names | one object `Crate_01`, materials `Wood_A` and `Metal_A` |
| Materials | single-sided, no textures |
| Validation | 0 errors, 0 warnings; 2 infos for unused UVs, which are kept for later texturing |
| File | 23 KB GLB |
| Look | multi-angle sheet reviewed: [look-sheet.png](look-sheet.png) |
| Engine | loads at the right scale, origin and orientation: [engine-check.png](engine-check.png) |

## What broke, and what each step caught

1. **Build 1 passed every number check and still looked wrong.**
   The metal corner caps shared their outer faces with the wood beams, so they showed only as small grey squares and would flicker (z-fighting) in a game.
   The diagonal braces stood only 1 cm off the body and read as thin lines at 4 m.
   Only the look step caught this.
   Fix: the caps sit 1 cm proud of the frame and the frame 5 cm proud of the body, so no two faces are coplanar.
2. **Inspect caught double-sided materials.**
   Blender leaves backface culling off, which exports `doubleSided: true` and makes the engine draw the inside of every closed mesh.
   Validation alone did not flag it, because it is legal glTF.
   Fix: turn on backface culling for each material, now a scripted check.
3. **The engine check caught black metal.**
   A fully metallic material reflects its surroundings, so in a Three.js scene without an environment map it renders almost black.
   Fix in the scene, not the asset: add an environment map (a CC0 Poly Haven HDRI in a real game, or the built-in RoomEnvironment for checks).
4. **Color has to be judged in the engine.**
   Blender's Workbench look renders do not show final lighting, and the same wood went from dark brown to pale tan under brighter engine lights.
   The look sheet is for shape and proportion; color and material are judged in the engine under the game's lighting.
5. **Three.js renames multi-material meshes.**
   One Blender object with two materials loads as a group `Crate_01` holding meshes `Crate_01_1` and `Crate_01_2`.
   Game code should find props by the group name, not the mesh names.
6. **My own viewer bug:** it did not handle a window resize, so the first screenshot left the bottom of the frame empty.
   Fixed with a resize handler.

## Still to do for issue #2

- Install MCP for Blender with safe mode on and telemetry off once the owner approves, then repeat this brief through the live bridge and its `look` tool and compare.
- Then make a 5 to 10 piece kit in the same style, as the article's adoption plan suggests.

Raw renders go to `look/`, which is ignored by git; the build script recreates them.
