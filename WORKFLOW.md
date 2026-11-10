# Our game-building workflow

The best way we currently know to build browser games, and later blockchain games, merged from the reviewed sources in `sources/`.
Each step names the note it came from.
When a new source improves a step, update this file and cite the note.

## Pipeline

1. **Concept video.** Generate a 10 to 15 s gameplay clip of one original concept built around one verb, with a steady playable camera and no on-screen text. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md), via Video2Game)
   For a phone-first game ask MiniMax H3 Max for 9:16, so the video shows the portrait framing the game needs; Lantern River's one take showed the camera, the hero and both key moments. ([Lantern River](https://github.com/imDev2023/lantern-river))
   One take was enough when the prompt named the art direction and the look of the props we already had (the kit's tan wood, braces and dark corners). ([calibration 4](calibration/2026-11-06-video2game/README.md))
   For a character, "camera behind the hero" was not enough: Brimful's golem faced the camera for the whole take, climbed with its back to the wall, and the gate, water and crate of the prompt's puzzle came out jumbled, while the world, palette and hero came out well.
   Take the look, world and hero from the video and the mechanic from the spec, and expect to draw the hero's back on the sheet. ([Brimful](https://github.com/imDev2023/brimful/blob/main/SPEC.md))
2. **Spec from frames.** Split the clip into frames and write the spec before any code: camera, hero, core mechanic, palette, light and the key moment. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
   Measure colours as 8 x 8 px averages of named frames, never by eye: under the video's warm grade its white wheelhouse measured tan. ([calibration 4](calibration/2026-11-06-video2game/README.md))
   Measure the lens too: the distance and field of view decide the look as much as the palette does. ([calibration 4](calibration/2026-11-06-video2game/README.md))
3. **Assets, cheapest source first.**
   A generator makes only what code cannot make well: the few solid hero objects that carry the look.
   Simple shapes (walls, houses, stairs, bridges) are scripts with CC0 textures mapped at real size, and CC0 models dress the rest; Kensei's first pass looked flat and grey until that dressing and a look pass went in. ([Kensei](sources/2026-11-07-kensei-opus-blender-unity.md))
   Before any sheet, make one or two mood stills from the gameplay camera until the owner approves the look, and edit every sheet from them. ([Kensei](sources/2026-11-07-kensei-opus-blender-unity.md))
   Edit the stills from a frame of the concept video, told to take only its style and not its composition, so the world stays the one already approved; ask for two per call, since Lamplighter's first four came back with two side views although the prompt named the chase camera, and one gave the hero loose cloth it was told to leave out. ([Lamplighter](https://github.com/imDev2023/lamplighter))
   - Free CC0 libraries: Poly Haven textures, HDRIs and models, and Poly Pizza models filtered to CC0. ([Claude Code + Blender](sources/2026-11-04-lummox-claude-code-blender.md))
   - Agent-built in Blender: hard-surface props, modular kits and level blockouts written as Blender Python. ([Claude Code + Blender](sources/2026-11-04-lummox-claude-code-blender.md))
   - Generated and paid: characters and organic shapes from concept sheets lifted to 3D with Tripo, Meshy or Hunyuan3D on fal, then cleaned up in Blender. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
     Choose how it will be rigged before paying, keep the raw download untouched, and give image-to-3D a reference on studio grey with no text, since green fringes and labels end up in the geometry; skin hard-surface parts rigidly, one bone per part. ([VGD packs](sources/2026-11-06-chongdashu-aioriented-vgd.md))
     Generate from 3 or 4 views (front, left, back, right; fal's `tripo3d/h3.1/multiview-to-3d`), not one: from a single front image the generator invented a second tail.
     Label each view by what it shows, since sheets swap left and right, and leave off anything the game draws or moves separately (a held tool, a flame, a glowing lantern), or it is welded into the mesh. ([Kensei](sources/2026-11-07-kensei-opus-blender-unity.md))
     Check which way each profile faces before lifting (a left view faces the image's left edge): both of Lamplighter's sheets drew the left profile twice although the prompt named each side and its facing, so the right view was made by mirroring the left, and [`tools/cut_views.py`](https://github.com/imDev2023/lamplighter/blob/main/tools/cut_views.py) cuts a sheet into the four views on a flat canvas, dropping stray marks the generator left under the feet. ([Lamplighter](https://github.com/imDev2023/lamplighter))
     Then cut the model to its budget, below. ([Kensei](sources/2026-11-07-kensei-opus-blender-unity.md))
   - For a set of 2D props or sprites, ask for one sheet on a flat green background, edited from real reference images, and cut it up with our own script. ([VGD packs](sources/2026-11-06-chongdashu-aioriented-vgd.md))
   - With all 3D from the kit and the bridge, fal only paid for the video, two backdrop images and the sound: 2.67 USD for a game, against Video2Game's gallery median of 6.13 USD. ([calibration 4](calibration/2026-11-06-video2game/README.md))
4. **Blender asset loop** for every model, described below.
5. **Game build** in Three.js with keyboard, gamepad and touch input and a complete loop: goal, progression, feedback, end and restart. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
   - If a score may ever carry value, write the rules first as an integer simulation: ticks, micrometres, seeded randomness, no `Math.sin` and no wall-clock time, with `replay(seed, inputs)` as the server's check; Dockstack's replays gave the same hash in Chrome, Node and JavaScriptCore. ([calibration 4](calibration/2026-11-06-video2game/README.md))
   - The server's check replays the run with the same build of the rules, refuses a run that claims more ticks than the time since its seed was handed out allows, takes the player from a verified signature and never from the request body, and pays each reward once under a stable key. ([VGD packs](sources/2026-11-06-chongdashu-aioriented-vgd.md))
   - Generate levels in fixed chunks, each from the seed and its own index alone, so the renderer streams any chunk and stages can be any length; keep stages as data the rules read, so a new stage needs no rule change. ([Lantern River](https://github.com/imDev2023/lantern-river))
   - Make the level passable by construction (Lantern River keeps an open channel through every rock row) and prove it with a test pilot that plays the safe line on dozens of seeds: that pilot found gate posts standing in the channel, which no single test of the generator showed. ([Lantern River](https://github.com/imDev2023/lantern-river))
   - The page only reads the simulation; a `?debug` check that hashes the state after each tick and after drawing catches the renderer writing into it. ([calibration 4](calibration/2026-11-06-video2game/README.md))
   - Keep the number of lights in a Three.js scene fixed: adding a light per streamed object makes Three.js recompile every material, which stutters on phones, so move a small pool of lights to the nearest objects instead. ([Lantern River](https://github.com/imDev2023/lantern-river))
   - Give a portrait chase camera its payoff ahead of the hero: it sees only about 34 degrees across, so Lamplighter's lanterns, lit as the hero passed them, were never on screen until each lit post sent its light forward along the line to the next. ([Lamplighter](https://github.com/imDev2023/lamplighter))
   - The owner rejected a hasty jump (2026-11-08); the rework, waiting for the owner's verdict: about a second in the air, a crouch in the last strides before the edge, a jump clip played across the flight (push-off, tuck at the top, reach for the landing) rather than one held pose, blended in and out over about a seventh of the flight, and a dip on landing; a 0.6 s hop with the pose snapped on in 40 ms read as hasty.
     Keep the obstacle being jumped current until the landing is over: Lamplighter's lookup moved to the next alley 0.6 m past the edge, so every jump was cut off in mid-air. ([Lamplighter](https://github.com/imDev2023/lamplighter))
   - Keep a runner's chase camera low and pitched almost level at a fixed height: pitched down from high up, it looked into each gap as it passed and the next roof slid up into the frame, and a camera that followed the jump's height with a lag made it worse. ([Lamplighter](https://github.com/imDev2023/lamplighter))
   - Playtest through the real input path: Lantern River's `tools/autoplay.js` steers by sending pointer drags to the page like a finger, and the recorded run replayed in Node to the same hash. ([Lantern River](https://github.com/imDev2023/lantern-river))
   - Give portrait screens their own framing: fitting a landscape span into a phone's width leaves a thin strip of game. ([calibration 4](calibration/2026-11-06-video2game/README.md))
6. **Look match and playtest.** Compare game and video frames side by side at fixed times, and let the agent play the game and record its best seconds. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
   - Play through scripts, not model sessions: Kensei's agent playthrough found real blockers but was slow and among his dearest sessions, while a scripted pilot like Lantern River's is cheap and repeatable; feel is judged by the owner playing, and the list of what feels wrong becomes the next brief. ([Kensei](sources/2026-11-07-kensei-opus-blender-unity.md))
   - Do the look in one look-only pass against the approved mood still, with before and after shots from the same spot and the frame rate before and after. ([Kensei](sources/2026-11-07-kensei-opus-blender-unity.md))
   - Dress a level by rule: clusters of 3 to 7 items at varied heights rather than rows, real-world logic in what sits beside what, the player's route kept clear; then snap every item onto the surface below it and list anything that moved by more than 1 cm. ([Kensei](sources/2026-11-07-kensei-opus-blender-unity.md))
   - Look, then measure: print the numbers (heights, gaps, distances to the route) next to every screenshot, since the bugs that mattered, a bridge floating 2.8 m up and a pickup out of jumping reach, looked fine. ([Kensei](sources/2026-11-07-kensei-opus-blender-unity.md))
   - Let a second agent judge the screenshots against the reference without seeing the builder's reasoning, with camera, lens, light and seed fixed and from the gameplay camera's distance. ([VGD packs](sources/2026-11-06-chongdashu-aioriented-vgd.md))
   - The pairs catch what no single screenshot does: the first Dockstack pairs showed a flat 30-degree side view where the video had a close 45-degree lens, front light and a quay receding into haze. ([calibration 4](calibration/2026-11-06-video2game/README.md))
   - A generated sky plate already carries the video's grade: leave tone mapping off and warm the lights rather than grading the frame twice, and apply any highlight shoulder to the brightest channel, since per-channel compression turned warm haze green. ([calibration 4](calibration/2026-11-06-video2game/README.md))
   - For a night scene, do the light before the models: glowing emissives with bloom, a mirror on the water stretched into streaks, haze and a deep sky turned Lantern River's grey-box from flat boxes into the video's mood with no new assets. ([Lantern River](https://github.com/imDev2023/lantern-river))
     Three.js's stock `Water` reflects only about 10% at a low chase camera, so the canal uses `Reflector` with its own shader; its reflection camera is cloned from the main one on first use, so leave a layer out of the mirror with `getReflectionCamera(camera).layers.disable(n)`, and keep things that burst overhead (fireworks) out of it or they land beside the hero as blobs. ([Lantern River](https://github.com/imDev2023/lantern-river))
     Merge each streamed chunk's static meshes into one per material, since a mirror draws the scene twice. ([Lantern River](https://github.com/imDev2023/lantern-river))
   - Size a backdrop plate for the widest lens and aspect, and check 2560 x 1080 and a 390 x 844 portrait before calling the look done. ([calibration 4](calibration/2026-11-06-video2game/README.md))
   - The skill's recorder captures at 27 to 47 fps on this Mac, below the game's own 60; read the game's frame rate from its `?debug` overlay instead. ([calibration 4](calibration/2026-11-06-video2game/README.md))
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
- Look twice after a build, since the first Material Preview look can come back grey while EEVEE compiles shaders.
  Wireframe and solid looks frame much tighter than Material Preview at the same `distance`, so leave theirs unset. ([calibration 2](calibration/2026-11-06-crate-bridge/README.md), [kit](calibration/2026-11-06-kit/README.md))
- If the first status call fails with a broken pipe, call it again: the server was still connected to an earlier Blender. ([kit](calibration/2026-11-06-kit/README.md))
- The official [Blender Lab MCP](https://www.blender.org/lab/mcp-server/), also offered as Anthropic's Claude Blender connector, is the alternative once we move to Blender 5.1 or newer.
- Use one bridge per project.
- The bridge is a workbench, not the source: write anything that works live back into the build script, and prove it with a clean headless rebuild. ([VGD packs](sources/2026-11-06-chongdashu-aioriented-vgd.md))
  Run headless builds with `--python-exit-code 1`, since a Python error otherwise still exits 0.

### Safety

- Keep the add-on's socket (port 9876) on localhost, since it has no authentication and safe mode guards only the MCP path, not raw code from other local processes.
- Keep safe mode on, and turn it off only for a specific task that needs file or network access, after saving.
- Save the `.blend` file before any large script run.
- Leave Blender's auto-run of Python scripts off, especially for downloaded `.blend` files.
- Add no Premium plan or generator API keys to the add-on without approval, because its 3D generation calls cost money.

### Scripts through the bridge

Safe mode checks each `execute_blender_code` script before it reaches Blender, so scripts follow its rules. ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))

- Make every call self-contained: a name defined in an earlier call is rejected, so nothing carries over between calls and state lives only in `bpy.data`.
- Define no classes: safe mode rejects a `class` statement, so helpers that share state take a dict. ([calibration 4](calibration/2026-11-06-video2game/README.md))
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
  Neighbouring parts that share a material and facing, such as planks in a stack, merge the same way; alternate their tone through the color attribute. ([kit](calibration/2026-11-06-kit/README.md))
- No two faces are coplanar and overlapping, since such parts flicker in the engine (z-fighting). ([calibration 1](calibration/2026-11-05-crate/README.md))
  Calibration 2's `checks.py` tests this by script. ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))
  Run it after every build, not only before export: in the kit it caught caps whose undersides shared a lid's plane, which no look showed, so a part stands proud on every face, including the one underneath. ([kit](calibration/2026-11-06-kit/README.md))
- Every material is used by at least one face; checking slot names alone misses faces that all landed on one slot. ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))
  Check the materials the pieces use, not everything in the file, since the GUI's startup file holds an unused grease-pencil material. ([kit](calibration/2026-11-06-kit/README.md))
- `npx @gltf-transform/cli validate <file>` reports zero errors, and `inspect` matches the brief.
- Each asset type (static, rigid-animated, skinned) has one export recipe, proved once with a deliberately lopsided marker asset so a mirrored axis shows; the game refuses a model whose triangle count, bounds, ground contact or facing differ from its manifest. ([VGD packs](sources/2026-11-06-chongdashu-aioriented-vgd.md))
- Materials on closed meshes are single-sided: turn on backface culling in Blender, or the GLB exports `doubleSided: true`. ([calibration 1](calibration/2026-11-05-crate/README.md))
- The GLB loads in our Three.js scene at the right scale, origin and orientation, and its colors read as briefed under the game's lighting.
- Names are clean, with no `Cube.003` and no leftover `.001` objects, including UV maps and color attributes (`bmesh` names a new UV map `Float2`). ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))
- `CREDITS.md` lists every pulled or generated asset with its source and licence.

Scripted versions:

- [calibration/2026-11-05-crate](calibration/2026-11-05-crate/README.md): a headless build with look renders, and the Three.js engine check page, which takes any GLB as `viewer.html?src=<path>`, or several `src` values for a lineup.
- [calibration/2026-11-06-crate-bridge](calibration/2026-11-06-crate-bridge/README.md): the bridge calls, with the Blender-side done checks as one script.
- [calibration/2026-11-06-kit](calibration/2026-11-06-kit/README.md): six pieces from one build script through the bridge, with the done checks and exports run per piece; the template for a set.
- [calibration/2026-11-06-video2game](calibration/2026-11-06-video2game/README.md): scene pieces with their pivots at the origin (a jib's hinge, a hook's tip, a boat's waterline), placed in a layout for looks, checked in mesh coordinates and exported at their origins.

### Engine notes

- Read each Poly Haven texture's real size from its API (`/info/<id>`, `dimensions` in millimetres) before mapping it: at a phone's resolution true-size roof tiles blurred into flat grey, so Lamplighter draws them half as large again, which also suits a stylised look. ([Lamplighter](https://github.com/imDev2023/lamplighter))
- In Three.js r186 a fragment shader reads an instance's colour as `vColor` (a vec4, under `USE_COLOR`), and `vViewPosition` points from the surface to the camera; one instanced mesh then holds lit and unlit lanterns by driving emission from the instance colour. ([Lamplighter](https://github.com/imDev2023/lamplighter))
- Metallic materials render almost black without an environment map, so every game scene sets `scene.environment` from a CC0 Poly Haven HDRI. ([calibration 1](calibration/2026-11-05-crate/README.md))
- Three.js loads a Blender object with several materials as a group of meshes named `<Name>_1`, `<Name>_2`, so game code finds props by the group name. ([calibration 1](calibration/2026-11-05-crate/README.md))
- glTF vertex colors (`COLOR_0`) multiply the base color, and Three.js applies them without setup.
  Blender exports a color attribute when the material multiplies it into Base Color through a Mix node, and keeps the other Mix input as the base color factor. ([calibration 2](calibration/2026-11-06-crate-bridge/README.md))

### Cutting a generated or scanned model to budget

A model with one texture atlas, as every Tripo output so far, keeps its own UVs and textures: weld, simplify with meshoptimizer and resize the textures ([`tools/simplify.sh`](https://github.com/imDev2023/lamplighter/blob/main/tools/simplify.sh)).
That took Lamplighter's hero from 1.93 million triangles to 24,000 with the face as generated, where the bake below left seams and dark blotches on it: its cage reaches 2% of the model's size, so from the forehead it hits the hair. ([Lamplighter](https://github.com/imDev2023/lamplighter))
Use the bake for models with several materials or overlapping UVs.

Generated models arrive at about 2 million triangles and scans at tens of thousands, both too heavy for a phone. ([Kensei](sources/2026-11-07-kensei-opus-blender-unity.md))
[Lantern River's `tools/lowpoly_bake.py`](https://github.com/imDev2023/lantern-river/blob/main/tools/lowpoly_bake.py) cuts one headless:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 \
  -P tools/lowpoly_bake.py -- in.glb out.glb --tris 6000 --size 1024
```

- It decimates a copy, unwraps it afresh, and bakes colour, a tangent-space normal map and roughness-metal from the original, then exports a single-sided GLB.
- Bake colour as emission, never as diffuse: on Poly Haven's brass candleholders the diffuse bake rendered black in Three.js, since metal has no diffuse colour. ([Kensei](sources/2026-11-07-kensei-opus-blender-unity.md))
- Measured on Poly Haven's mossy rock set: 63,127 triangles to 6,000 in 4.5 s, 828 KB, then 481 KB after `gltf-transform optimize --compress meshopt --texture-compress webp`, and it read like the original at viewing distance. ([Kensei](sources/2026-11-07-kensei-opus-blender-unity.md))

### What agents model well

- Well: hard-surface props, modular kits on a grid, environment blockouts, batch cleanup, export pipelines and LOD scaffolding.
- Badly: hero characters, foliage, cloth and ornate props, which need generators plus cleanup, a library, or an artist.
- To make a set, approve one piece, then ask for variants in the same style and grid.
  - First turn the approved piece's build into a function of its size and rebuild the piece from it: its GLB must come out byte-identical, which proves every variant starts from the approved look. ([kit](calibration/2026-11-06-kit/README.md))
  - Build the whole set in one script with every piece at the origin, hide the others to look at one, and export each by selection. ([kit](calibration/2026-11-06-kit/README.md))

### Rigging a generated character in code

[`tools/rig_hero.py`](https://github.com/imDev2023/lamplighter/blob/main/tools/rig_hero.py) rigs an A-posed humanoid headless with Mixamo bone names and keys a run cycle and a jump pose by aiming bones at target directions. ([Lamplighter](https://github.com/imDev2023/lamplighter))

- Measure joints from the mesh and print them: a gap test for the torso's width failed on a simplified mesh (2 cm gaps open anywhere), so the shoulders come from a line fitted through each arm.
- Bone heat weighted no vertex on the generated mesh's layered cloth; solving it on a watertight voxel copy and transferring the weights by nearest face worked every time, in about 5 s.
- Around a tunic's hem, hand part of each thigh's weight to the hips, or the trousers push through the hem as the leg swings.
- Blender's glTF exporter samples one frame past an action's end: pin the end to the last frame before the loop closes, or a 20-frame cycle exports as 21 and hitches.
- Check every rig in a Three.js page with the skeleton drawn, from the side at several moments of the clip, and up close on the face.
- For a natural run, retarget one from Quaternius's Universal Animation Library (CC0) with `--motion` rather than keying it: aim each bone along the line between the same two source joints, which carries over any difference in proportions and rest pose, scale the hips' offsets by leg length, and play the clip at the ground speed its planted foot implies so the feet do not skate. Take out about half of a sprint's forward lean and keep the head level, or the face hides and a held prop points down. Mixamo motion cannot go into a CC0 public repo under Adobe's terms. ([Lamplighter](https://github.com/imDev2023/lamplighter), 2026-11-09)

## Ship check

- Set a first-load download budget, compress models with `gltf-transform optimize` (meshopt or Draco geometry, KTX2 textures), and load levels on demand. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
  Dockstack compresses in a `build.sh` step, keeping Blender's exports as sources: models went from 398 KB to 146 KB, and the whole game loads 1.40 MB plus Three.js. ([calibration 4](calibration/2026-11-06-video2game/README.md))
- Downmix stereo sound to mono with an explicit `pan=mono|c0=0.5*c0+0.5*c1`, since ffmpeg's `-ac 1` makes correlated stereo about 3 dB hotter, and give clips under 3 s a constant gain capped by true peak, since `loudnorm` overshoots them. ([calibration 4](calibration/2026-11-06-video2game/README.md))
- Remove test and unused assets from the build; Sumiro shipped a 14 MB test model. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
- Add touch controls and test on a phone. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
- For a private phone preview on Vercel's hobby plan, deploy without `--prod`: deployment URLs sit behind Vercel sign-in, but the first `vercel deploy` of a new project becomes its production deployment and gets a public `<project>-<word>.vercel.app` alias. Check every URL the deploy prints with `curl -w "%{http_code}"` (a 302 is protected, a 200 is public), remove a public alias with `vercel alias rm`, and check the page through `vercel curl --deployment <url>`. ([Lamplighter](https://github.com/imDev2023/lamplighter), 2026-11-09)
- Prefer CC0 assets, keep CC-BY credits in `CREDITS.md`, and check each generator's commercial terms. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md), [Claude Code + Blender](sources/2026-11-04-lummox-claude-code-blender.md))
- Never pay out on a score the browser reports; verify it on a server. ([Sumiro](sources/2026-11-04-xikhar-sumiro.md))
- Upload nothing without a passing smoke test, ship the exact package that was tested rather than a rebuild, and keep video masters out of git. ([VGD packs](sources/2026-11-06-chongdashu-aioriented-vgd.md))

## Costs

- Free: Blender, both bridges, Poly Haven, Poly Pizza, Three.js, and Claude Code within our plan.
- Paid, with approval each time: fal calls (video, images, image-to-3D), OpenAI image calls, and generator API keys or Premium in MCP for Blender.
- fal prices checked on 2026-11-06: MiniMax H3 Max video 0.112 USD per second at 1080p until 2026-11-15 and 0.16 after, Nano Banana Pro images 0.15 each at 1K or 2K, Meshy image-to-3D 1.20 with textures, ElevenLabs sound 0.002 per second and music 0.60 per started minute. ([calibration 4](calibration/2026-11-06-video2game/README.md))
- Tripo on fal, checked on 2026-11-07: every Tripo endpoint, including H3.1 multiview-to-3D, bills 0.01 USD per credit; Kensei paid 60 credits (0.60 USD) for detailed geometry and 40 for standard, through Tripo's own API, and 8.20 USD for a level's 16 models. ([Kensei](sources/2026-11-07-kensei-opus-blender-unity.md))
- Send `x-app-fal-disable-fallback: true` so a run uses only the model asked for, and log each run's `x-fal-request-id` and `x-fal-billable-units` headers; the cost some endpoints return in the body is a placeholder. ([VGD packs](sources/2026-11-06-chongdashu-aioriented-vgd.md))
- Read the exact charge from fal's usage API (`GET https://api.fal.ai/v1/models/usage`, filtered by `endpoint_id` and the run's `start` and `end`) with `FAL_BILLING_KEY` from the global env, a read-only BILLING-preset key; the model key `FAL_KEY` cannot read it. ([calibration 4](calibration/2026-11-06-video2game/README.md))
- fal bills music per started minute and sound effects per started second, and outputs run slightly long: ask for 59 s of music, not 60, or a 24 ms overrun doubles the price. ([calibration 4](calibration/2026-11-06-video2game/README.md))
