# Our game-building workflow

The best way we currently know to build browser games, and later blockchain games, merged from the reviewed sources in `sources/`.
Each step names the note it came from.
When a new source improves a step, update this file and cite the note.

## Pipeline

1. **Concept video.** Generate a 10 to 15 s gameplay clip of one original concept built around one verb, with a steady playable camera and no on-screen text. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md), via Video2Game)
2. **Spec from frames.** Split the clip into frames and write the spec before any code: camera, hero, core mechanic, palette, light and the key moment. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
3. **Assets, cheapest source first.**
   - Free CC0 libraries: Poly Haven textures, HDRIs and models, and Poly Pizza models filtered to CC0. ([Claude Code + Blender](sources/2026-11-04-lummox-claude-code-blender.md))
   - Agent-built in Blender: hard-surface props, modular kits and level blockouts written as Blender Python. ([Claude Code + Blender](sources/2026-11-04-lummox-claude-code-blender.md))
   - Generated and paid: characters and organic shapes from concept sheets lifted to 3D with Tripo, Meshy or Hunyuan3D on fal, then cleaned up in Blender. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
4. **Blender asset loop** for every model, described below.
5. **Game build** in Three.js with keyboard, gamepad and touch input and a complete loop: goal, progression, feedback, end and restart. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
6. **Look match and playtest.** Compare game and video frames side by side at fixed times, and let the agent play the game and record its best seconds. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
7. **Ship check**, described below, before anything goes live.

## Blender asset loop

Inspect the scene, write the brief, build, look, fix, check, export, then verify in the game. ([Claude Code + Blender](sources/2026-11-04-lummox-claude-code-blender.md))

### Bridge

Use [MCP for Blender](https://github.com/ahujasid/mcp-for-blender), which works with our Blender 4.3, with telemetry off and safe mode on:

```bash
claude mcp add blender -e DISABLE_TELEMETRY=true -e BLENDER_MCP_SAFE_MODE=1 -- uvx mcp-for-blender
uvx mcp-for-blender install-addon
```

Its tools load only in a Claude Code session started after the install.
Launch Blender's GUI with the add-on enabled for that run, which leaves Blender's preferences unchanged; the add-on then starts its server on localhost:9876 by itself, about 50 s after launch. ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))

```bash
BLENDERMCP_NO_UPDATE_CHECK=1 /Applications/Blender.app/Contents/MacOS/Blender --addons blender_mcp
```

The server needs the GUI and never starts under `blender -b`.
If it is not running, press `N` in the 3D viewport, open the MCP for Blender tab and start it.

- Use the bridge to author: looking live from any angle, distance and shading caught defects that fixed renders missed. ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))
- The official [Blender Lab MCP](https://www.blender.org/lab/mcp-server/), also offered as Anthropic's Claude Blender connector, is the alternative once we move to Blender 5.1 or newer.
- Use one bridge per project.

### Safety

- Keep the add-on's socket (port 9876) on localhost, since it has no authentication and safe mode guards only the MCP path, not raw code from other local processes.
- Keep safe mode on, and turn it off only for a specific task that needs file or network access, after saving.
- Save the `.blend` file before any large script run.
- Leave Blender's auto-run of Python scripts off, especially for downloaded `.blend` files.
- Add no Premium plan or generator API keys to the add-on without approval, because its 3D generation calls cost money.

### Scripts through the bridge

Safe mode checks each `execute_blender_code` script before it reaches Blender, so scripts follow its rules. ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))

- Make every call self-contained: a name defined in an earlier call is rejected, so nothing carries over between calls and state lives only in `bpy.data`.
- Import only `bpy`, `bmesh`, `mathutils` and pure-Python standard modules; `time`, `os`, `open()` and lambdas are rejected, so print reports and save them from the tool's output.
- Write the build as one script that reuses its materials, mesh and object by name, so rerunning it leaves no `.001` duplicates.
- Commit the final build, check and export calls; they also run headless with `blender -b --python`, which reproduced calibration 2's GLB byte for byte.
- Set a mesh's material slots before `bmesh.to_mesh()`, because `mesh.materials.clear()` afterwards resets every face to the first slot.
- Find shader nodes by type, never by name, since names are localized.

### Brief template

Our own template, adapted from the Claude Code + Blender article:

```text
First, report what is already in the open Blender scene.

Build <object> for <game>, seen from <camera and distance>.
- Size: <width> x <depth> x <height> m
- Budget: at most <N> triangles
- Style: <art direction in a few words, matching the concept video>
- Materials: PBR metallic-roughness: <list>, textures at most <size> px
- Names: object <Name_01>, materials <Material_A>
- Origin: <bottom center at Z=0 | hinge | socket>; apply location, rotation and scale
- Export: selected objects only, GLB, +Y up, to assets/models/<name>.glb

Then look at it in wireframe and Material Preview from several angles and once from the game camera's distance,
report the triangle count and bounds, fix anything that misses the brief, export, and list the file path and any warnings.
Do not stop until every done check passes.
```

### Done checks

- Measured bounds and triangle count match the brief.
- A person has looked at one multi-angle view, checking shape and proportion; color is judged later, in the engine.
- Details read face-on under flat lighting without shadows: judge them in Material Preview or the engine, never only in Workbench renders with cavity or outlines, which draw edges the engine does not.
  A detail that shares its material and facing with the surface behind it disappears; darken the recess with a color attribute, which costs no triangles or textures. ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))
- No two faces are coplanar and overlapping, since such parts flicker in the engine (z-fighting). ([calibration 1](calibration/2026-11-05-crate/README.md))
  Calibration 2's `checks.py` tests this by script. ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))
- Every material is used by at least one face; checking slot names alone misses faces that all landed on one slot. ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))
- `npx @gltf-transform/cli validate <file>` reports zero errors, and `inspect` matches the brief.
- Materials on closed meshes are single-sided: turn on backface culling in Blender, or the GLB exports `doubleSided: true`. ([calibration 1](calibration/2026-11-05-crate/README.md))
- The GLB loads in our Three.js scene at the right scale, origin and orientation, and its colors read as briefed under the game's lighting.
- Names are clean, with no `Cube.003` and no leftover `.001` objects, including UV maps and color attributes (`bmesh` names a new UV map `Float2`). ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))
- `CREDITS.md` lists every pulled or generated asset with its source and licence.

Scripted versions:

- [calibration/2026-11-05-crate](calibration/2026-11-05-crate/README.md): a headless build with look renders, and the Three.js engine check page, which takes any GLB as `viewer.html?src=<path>`.
- [calibration/2026-11-06-crate-bridge](calibration/2026-11-06-crate-bridge/README.md): the bridge calls, with the Blender-side done checks as one script.

### Engine notes

- Metallic materials render almost black without an environment map, so every game scene sets `scene.environment` from a CC0 Poly Haven HDRI. ([calibration 1](calibration/2026-11-05-crate/README.md))
- Three.js loads a Blender object with several materials as a group of meshes named `<Name>_1`, `<Name>_2`, so game code finds props by the group name. ([calibration 1](calibration/2026-11-05-crate/README.md))
- glTF vertex colors (`COLOR_0`) multiply the base color, and Three.js applies them without setup.
  Blender exports a color attribute when the material multiplies it into Base Color through a Mix node, and keeps the other Mix input as the base color factor. ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))

### What agents model well

- Well: hard-surface props, modular kits on a grid, environment blockouts, batch cleanup, export pipelines and LOD scaffolding.
- Badly: hero characters, foliage, cloth and ornate props, which need generators plus cleanup, a library, or an artist.
- To make a set, approve one piece, then ask for variants in the same style and grid.

## Ship check

- Set a first-load download budget, compress models with `gltf-transform optimize` (meshopt or Draco geometry, KTX2 textures), and load levels on demand. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
- Remove test and unused assets from the build; Sumiro shipped a 14 MB test model. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
- Add touch controls and test on a phone. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
- Prefer CC0 assets, keep CC-BY credits in `CREDITS.md`, and check each generator's commercial terms. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md), [Claude Code + Blender](sources/2026-11-04-lummox-claude-code-blender.md))
- Never pay out on a score the browser reports; verify it on a server. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))

## Costs

- Free: Blender, both bridges, Poly Haven, Poly Pizza, Three.js, and Claude Code within our plan.
- Paid, with approval each time: fal calls (video, images, image-to-3D), OpenAI image calls, and generator API keys or Premium in MCP for Blender.
