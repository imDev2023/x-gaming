# Chong-U Lim: the AIOriented repos (VibeGameDev packs)

- **Source:** [github.com/orgs/AIOriented/repositories](https://github.com/orgs/AIOriented/repositories), 22 repos
- **Author:** Chong-U Lim ([@chongdashu](https://x.com/chongdashu), [youtube.com/@AIOriented](https://www.youtube.com/@AIOriented)), who runs [vibegamedev.com](https://vibegamedev.com)
- **Access:** 20 repos are private to paying VibeGameDev members; the owner is one. Only `freecut` and `insiders-claude-code-statusline-tutorial` are public, so most links below work only for members.
- **Read on:** 2026-11-06, every repo and every branch, at the commits listed under "What was checked"

## Verdict

Useful, and the most useful source so far for how we build: no repo replaces our pipeline, but most of them sharpen a step of it.
The value is in the method, written down in about 500 learnings files from real builds: Blender driven by script with numeric gates, fal used with cost ledgers and green-screen sheets, blind visual critics, and release gates.
One pack, Retro del Sol, has the server-side replay check our leaderboard needs, in a working online game.
None of them has an integer simulation like Dockstack's, a leaderboard backend or anything on a blockchain.
Most of the games are 2D Phaser or Unity, so their code matters to us less than their records.

## What the repos are

Grouped by how much they help us.

### Most useful

- **vgd-skills** (v3.6.0): 24 agent skills for Claude Code and Codex covering Blender (headless, live over MCP, and into WASM), Three.js, fal images and video, Tripo, Meshy, Retro Diffusion 3D, Colyseus multiplayer, the Wavedash and CrazyGames portals, and session records (prompts, plans, learnings, a visual devlog, safe commits).
  We installed the 15 game-pipeline skills into this project (see "What helps us").
- **vgd-retro-del-sol**: an online delivery game on trikes and boats, built on the WASM template with a Colyseus world server on Fly, a Convex backend holding coins, items and a transaction ledger, Wavedash sign-in and 73 learnings files.
  Live at [retrodelsol.com](https://retrodelsol.com/).
- **vgd-cloudpost-harbor**: one stylized harbour scene built twice by agents, in Unity 6 and Unreal 5.8, from the same Blender exports, with a Meshy courier rigged by script in Blender and a 140-step illustrated devlog.
- **vgd-robo-tennis**: an arcade robot-tennis game in Unity with a WebGL build on Vercel and Wavedash, whose character was made in Meshy and then rigged and animated by Blender scripts.
- **vgd-pirate-isometric**: research turning one side-view pirate sprite into an eight-direction isometric turnaround and walk cycle with fal image and video models, with every run in a cost ledger.
- **vgd-point-click**: a 1950s drive-in point-and-click adventure in Phaser 4, built over 54 recorded sessions, with a data-driven puzzle language, fal-made props and ElevenLabs voices.
- **builderpack-threejs-dungeon-game**: a one-file Three.js stealth game on Quaternius's CC0 Cube World kit, shipped with the whole Claude Code session that built it.

### Partly useful

- **vgd-wasm-game-template** (v2.8.0): a kit for making a browser game by talking to an agent, with a small Rust engine compiled to WebAssembly, WebGPU rendering with a WebGL 2 fallback, a blank game, a demo arena game, pinned skills and release targets for Vercel, Wavedash and CrazyGames.
- **vgd-steampunk-platformer**: a five-level 2D platformer with eleven reusable prompts, one per build stage, and provenance files for every generated sound.
- **vgd-hero-quest**: a 2D platformer with an iOS build through Capacitor; its `start` and `main` branches are the before and after of a tutorial.
- **vgd-streets-of-vibes**: a 2D side-scrolling beat-'em-up with crowd AI and combat-feel work.
- **vgd-pirate-survival-beatemup**: a 17-lesson, 30-minute tutorial game, with `start` and `completed` branches.
- **vgd-pirate-platformer**: a portrait 2D Phaser platformer whose hero was made with GPT Image and Sora.
- **vgd-pirate-ios**: a Three.js point-and-click adventure wrapped for iPhone with Capacitor.
- **vgd-backyard-rascals**: three-a-side capture the flag in the WASM template against bots or online, with an authoritative Colyseus server and client prediction.
- **vgd-unity-2.5d-arena**: a Unity brawler with 2D sprite characters in a 3D arena, made with the author's Spriterrific sprite service.

### Not useful to us now

- **vma-skills** and **vma-apps**: the sister program's native iOS app skills and sample apps (paywall, onboarding, streaks, iCloud sync).
- **vgd-vibe-fighter**: a 2D fighting game with no build records.
- **freecut**: a public fork of a browser video editor, usable by hand but with no scripting interface.
- **insiders-claude-code-statusline-tutorial**: a tutorial for the Claude Code status line.
- **vgd-tactics**: empty.

## What the repos leave out

- **Integer or replay-checked scores.** The WASM engine steps at a fixed 120 Hz with seeded randomness, but in 32-bit floats, and works out its step count from wall time; every Phaser game uses `Math.random` and a variable frame time.
- **Leaderboards and a way to pay out.** The template's Wavedash adapter uploads a score straight from the browser, neither pack calls it, and Backyard Rascals' leaderboard is only an in-match scoreboard.
- **Blockchain.** No wallets, contracts or tokens anywhere; Retro del Sol's coins live in Convex.
- **Three.js games beyond two small ones.** Only the dungeon game and the iOS point-and-click use Three.js.
- **Costs for most runs.** Dollar figures appear in a handful of learnings files; most sessions record none.
- **Licences, consistently.** The six larger packs carry a VibeGameDev member licence, three README files say MIT with no licence file, and the rest state nothing.

## What was checked

- Cloned all 22 repos and every branch on 2026-11-06; five reviewers read them in parallel, and the key claims below were then re-read in the code.
- `vgd-skills` is at tag v3.6.0 (`a513c8c`); its fal skill does send `x-app-fal-disable-fallback: true` and records `x-fal-billable-units`.
- Retro del Sol's world server gives each player a step credit that grows at 1.25 times real time and refuses any input run larger than the credit (`game/server/src/room.ts`), and its game exports a `gym_tick(steps)` that advances a given number of steps.
  Its multiplayer learnings record no corrections for 40 honest bots and a client cheating at four times speed held to 1,608 steps in 10 s.
- Its economy pays a delivery once, under the ledger key `delivery:<id>`, and only the server holds the secret that can write to it.
- The template engine's clock runs whole `1/120` s steps in `f32`, at most 12 per call.
- Sizes from the learnings files: the blank game's WASM core is 24.4 KiB with no imports, Retro del Sol's 92 KB, and Retro del Sol's whole release 14.2 MB.
- Nothing was built or played this session; the live games are at retrodelsol.com, [wavedash.com/games/backyard-rascals](https://wavedash.com/games/backyard-rascals) and the `aiod.dev` and Vercel links in each README.

## What helps us

Merged into [WORKFLOW.md](../WORKFLOW.md), in our own words.

1. **Blender: script is the source, the live scene is a workbench.** Anything that works through the bridge is written back into the build script, and a clean headless rebuild proves it.
   Headless runs use `--python-exit-code 1`, since a Python error otherwise still exits 0.
2. **One tested export recipe per asset type**, proved with a deliberately lopsided marker asset, and an import that refuses a model whose triangle count, bounds, ground contact or facing differ from its manifest.
3. **A blind critic:** a second agent judges screenshots against the reference without seeing the builder's reasoning, from the gameplay camera's distance, with camera, lens, light and seed fixed.
4. **Generated 3D:** choose the rig route before paying, keep the raw download untouched, give image-to-3D a reference on studio grey with no text, and skin hard-surface parts rigidly.
5. **fal:** send `x-app-fal-disable-fallback: true` so a run uses only the model asked for, log each request ID with the `x-fal-billable-units` header, and ask for a set of props as one sheet on flat green, cut up by our own script.
6. **Server checks for scores:** replay with the same build of the rules, refuse runs that claim more ticks than the elapsed time allows, read the player from a verified signature never from the request body, and pay each reward once under a stable key.
7. **Release gates:** no upload without a passing smoke test, ship the exact package that was tested, and keep video masters out of git.

## Blockchain fit

- Retro del Sol's server pattern carries straight over to Dockstack's verifier: a Cloudflare Worker replays `{ seed, releases }` with the game's own `sim.js`, a wallet signature replaces the Wavedash login token, and a speed check compares the run's ticks with the time since the seed was handed out.
- A one-time key per reward, as in its ledger, is what a contract or Worker needs to stop a run being paid twice.
- The Wavedash notes warn that a hosted game runs inside a portal's iframe, where popups are blocked; a wallet connect would need its own page or an injected provider.
- Retro Diffusion's terms forbid using its outputs to train AI and ask that any repo passing them on say so, which matters before such assets go into a public repo or an NFT.

## Where the copies live

- Every repo is cloned locally under `reference/aioriented/`, which is gitignored and stays on this Mac.
- The 15 game-pipeline skills from vgd-skills v3.6.0 are copied into `.claude/skills/`, also gitignored: blender-headless, blender-mcp-live, blender-wasm-webgpu, threejs-builder, fal-ai-image, fal-ai-video, meshy, tripo, retro-diffusion-3d, colyseus-multiplayer, wavedash, crazygames, capture, journey and git-commits.
  The fal, Meshy, Tripo and Retro Diffusion skills spend credits, so each run still needs the owner's approval.

## Next step

Use the Retro del Sol pattern for the verifier in [issue #4](https://github.com/imDev2023/x-gaming/issues/4), and put the Blender loop's new gates (export recipe, import gate, blind critic) through the next asset calibration.
