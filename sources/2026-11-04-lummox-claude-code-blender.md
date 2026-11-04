# Lummox: Claude Code + Blender as a game-asset pipeline

- **Source:** [x.com/Lummox_eth/status/2117215758472073446](https://x.com/Lummox_eth/status/2117215758472073446) (an X Article)
- **Author:** Lummox ([@Lummox_eth](https://x.com/Lummox_eth))
- **Posted:** 2026-11-02, about 10.8K views when read
- **Read on:** 2026-11-04

## Verdict

It helps, mostly by tightening the Blender stage of our current workflow rather than by adding a new capability.
The useful parts are a disciplined asset loop (brief, build, look, fix, check, export, verify in the engine), a definition of done that would have caught Sumiro's 100 MB of models, and a live Blender bridge that lets the agent see what it built.
The bridge it recommends is real, works with our installed Blender 4.3 today, and pulls free CC0 assets that cut both generation cost and rights risk.
It is a written guide, not a demonstration: its one screenshot is borrowed from the tool's README and shows a different app making a pyramid.
Worth adopting with the safety settings below, and trying it costs nothing.

## What the article says

The core idea: Claude Code decides, Blender executes, a person reviews, and the game engine receives a clean GLB.
Games need named objects at the right scale, sensible origins, materials that survive export and triangle counts within budget, not one impressive render.

- **Why Claude Code fits:** it holds project rules (scale, naming, budgets, style), writes and iterates Blender Python (`bpy`), drives Blender as a live tool through MCP, and keeps going until checks pass.
- **Blender stays the source of truth.** Meshes, materials, UVs, modifiers and armatures live in Blender, and the agent drives it rather than replacing it.
- **Two ways to connect:** the official Blender Lab MCP (behind Anthropic's Claude Blender connector), or the community `mcp-for-blender`, added to Claude Code with `claude mcp add blender uvx mcp-for-blender`.
  Use one bridge per project.
- **The loop:** inspect the scene, write a brief with numbers, build (blockout first, then refine), look at the result from several angles, fix, check the numbers, export, and verify inside the engine.
  Skipping the look step produces confident nonsense, such as a 1 m crate that turns out 17 m tall.
- **Export is its own stage:** meters, applied transforms, origins where gameplay expects them, GLB for web and Godot, clean names, and credits for anything pulled in.
- **Where it works:** hard-surface props, kits with consistent naming and grid sizes, environment blockouts, batch cleanup of messy files, export pipelines, LOD scaffolding, and learning `bpy` by reading what the agent runs.
- **Where it does not:** hero organic characters, foliage, cloth and ornate props.
  For those, use generators plus retopology and baking, asset libraries, or an artist.
- **Brief like a technical artist:** exact size in meters, a triangle budget, style, PBR materials, object and material names, origin rules and the export target, followed by a required look-and-report pass.
- **Failure modes:** claimed success without a screenshot, wrong scale, wrong origin, names like `Cube.003`, over-promised organic shapes, unsafe Python, MCP port confusion, and missing credits.
- **Adoption plan:** a calibration week that connects the bridge, writes a rules file, takes one prop into the engine, turns that into a checklist and a small validation script, and ends with a 5 to 10 piece kit.
- **Done means:** measured bounds and triangle count match the brief, a person saw a multi-angle view, the file opens in the engine at the right scale, names are clean, and credits are updated.

## What the article leaves out

- **Evidence.** There is no game, asset or session of the author's own.
  Its single screenshot is the `mcp-for-blender` README's own image of the ChatGPT/Codex app making a wooden pyramid, not Claude Code.
- **Links.** No tool is linked, so the names had to be matched to the real projects below.
- **Version requirements.** The official Blender Lab add-on needs Blender 5.1 or newer.
- **Security.** Both bridges run model-written Python inside Blender with the user's full file access.
- **Telemetry and a paid tier** in the community tool (details below).
- **Our engine.** It mostly targets Godot, Unity and Unreal; for Three.js, GLB is the right format and the same checks apply.

## What I checked

Checked on 2026-11-04.

- **`mcp-for-blender` is real and established.**
  It is the renamed `blender-mcp` by Siddharth Ahuja ([github.com/ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender), MIT, about 33K stars, PyPI version 2.2.6), and the old package name now installs the new one.
  It states it is not affiliated with the Blender Foundation.
  The article's install command matches its README.
- **Its tools:** run Python in Blender; `look` at the viewport, a camera, an auto-framed multi-angle sheet or an animation strip, drawn solid, material, rendered, wireframe or X-ray; a compact scene summary; one-call 3D generation (Tripo, Hunyuan3D, Hyper3D Rodin, Meshy); asset search and import (Poly Haven, Sketchfab, Poly Pizza); add-on status; and telemetry controls.
- **It works with what we have.** It needs Blender 3.0 or newer, Python 3.10 or newer and `uv`; this Mac has Blender 4.3.0 and `uvx`.
- **Security, from its README:** the add-on's socket (port 9876) has no authentication or encryption, so anything that can reach it can run Python in Blender.
  By default the agent can run any Python.
  `BLENDER_MCP_SAFE_MODE=1` blocks direct file access, running other programs, network access and code that persists after a script, while modeling, rendering, saving and import or export still work.
- **Telemetry:** collecting prompts, code, screenshots and scene data is opt-in, but a minimal anonymous usage record (install ID, tool name, success, timing, versions, OS) is sent by default.
  `DISABLE_TELEMETRY=true` turns off all of it.
- **Paid tier:** a Premium plan generates 3D models without your own API keys, and the tool prefers Premium generators automatically, so a generation call can cost money.
- **The official server is real.** Blender Lab, the Blender Foundation's experimental space, publishes it at [blender.org/lab/mcp-server](https://www.blender.org/lab/mcp-server/), with source at projects.blender.org/lab/blender_mcp.
  Add-on version 1.0.3 requires Blender 5.1 or newer.
  Its page shows scene analysis, renaming, data-relation queries, scene debugging and explaining Geometry Nodes setups.
  It warns that the server runs model-generated code with no guard against data being deleted or sent elsewhere, and recommends a virtual machine or a computer without sensitive data.
- **Anthropic's connector is the same effort.** Anthropic announced on 2026-04-28 that the Blender developers built an MCP connector now officially available for Claude, alongside a one-time donation to Blender ([anthropic.com/news/claude-for-creative-work](https://www.anthropic.com/news/claude-for-creative-work)).
- **Asset licences:** every Poly Haven asset is CC0 (about 2,400 HDRIs, textures and models, free, no credit required).
  About 69% of Poly Pizza is CC-BY and needs credit; the tool stores the credit line on each imported object and can filter to CC0.
  Sketchfab licences vary per model.
- **Replies:** none of the visible replies discussed the article.

## How it improves our workflow

Our pipeline so far (from the [Sumiro note](2026-11-04-xikhar-sumiro.md)) already has a Blender cleanup step through Atlas's `model3d-gen` skill, which runs Blender headless from scripts.
This article adds five things:

1. **Eyes on the Blender step.** The `look` tool lets the agent check its own work from several angles before export instead of editing blind.
2. **Free assets first.** Poly Haven and CC0 Poly Pizza can replace paid generation for textures, HDRIs, props and environment pieces.
3. **Numbers in every brief and a hard definition of done.** Triangle budgets, real sizes and a validation pass would have caught Sumiro's 100 MB of models and its leftover 14 MB test file.
4. **Credits tracking**, which we need anyway before anything is sold.
5. **A clear split of labor:** agent-written geometry for hard-surface props, kits and blockouts; generators plus cleanup for characters and organic shapes.

These are merged into [WORKFLOW.md](../WORKFLOW.md).

## Blockchain fit

- **CC0 assets are the safest base for anything sold on-chain**, since no one else's rights or credits come attached.
- **Clean, consistent object names become engine names and can become token trait names**, so an item kit maps directly onto collection metadata.
- **Approving one piece and then asking for variants in the same style** suits item sets with rarity tiers.
- **Triangle budgets and export checks** keep a game light enough for players on phones.
- **Security matters more on a crypto developer's machine.**
  Without safe mode, model-written Python inside Blender can read any file the user can, including env files and wallet keys.
  Keep safe mode on, the socket on localhost, and Blender's auto-run of scripts in downloaded `.blend` files off.

## Also found while checking (not evaluated yet)

- [arjun988/blender-skills](https://github.com/arjun988/blender-skills) (MIT, about 1.7K stars, last updated 2026-07-10): 94 Blender skills for Claude Code and other agents, with LOD, collision, optimization and engine-export steps.

## Possible next step

Run the calibration task, which needs no paid calls: install `mcp-for-blender` with safe mode on and telemetry off, take one hard-surface prop from a brief to a GLB loaded in a Three.js scene, and record what broke.
Tracked in [issue #2](https://github.com/imDev2023/x-gaming/issues/2).
