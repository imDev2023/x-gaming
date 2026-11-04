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

- Use [MCP for Blender](https://github.com/ahujasid/mcp-for-blender), which works with our Blender 4.3, with telemetry off and safe mode on:

  ```bash
  claude mcp add blender -e DISABLE_TELEMETRY=true -e BLENDER_MCP_SAFE_MODE=1 -- uvx mcp-for-blender
  uvx mcp-for-blender install-addon
  ```

  Then press `N` in Blender's 3D viewport, open the MCP for Blender tab, and start the server if it is not running.
- The official [Blender Lab MCP](https://www.blender.org/lab/mcp-server/), also offered as Anthropic's Claude Blender connector, is the alternative once we move to Blender 5.1 or newer.
- Use one bridge per project.

### Safety

- Keep the add-on's socket (port 9876) on localhost, since it has no authentication.
- Keep safe mode on, and turn it off only for a specific task that needs file or network access, after saving.
- Save the `.blend` file before any large script run.
- Leave Blender's auto-run of Python scripts off, especially for downloaded `.blend` files.
- Add no Premium plan or generator API keys to the add-on without approval, because its 3D generation calls cost money.

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

Then show solid and wireframe views from several angles, report the triangle count and bounds,
fix anything that misses the brief, export, and list the file path and any warnings.
Do not stop until every done check passes.
```

### Done checks

- Measured bounds and triangle count match the brief.
- A person has looked at one multi-angle view.
- `npx @gltf-transform/cli validate <file>` reports zero errors, and `inspect` matches the brief.
- The GLB loads in our Three.js scene at the right scale, origin and orientation.
- Names are clean, with no `Cube.003` and no leftover `.001` objects.
- `CREDITS.md` lists every pulled or generated asset with its source and licence.

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
