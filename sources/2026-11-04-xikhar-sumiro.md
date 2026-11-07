# Sumiro: "a full original game in 24 hours using AI"

- **Source:** [x.com/xikhar/status/2117776295534997818](https://x.com/xikhar/status/2117776295534997818)
- **Author:** Shikhar ([@xikhar](https://x.com/xikhar), [github.com/xikhar](https://github.com/xikhar))
- **Posted:** 2026-11-04, a 7-post thread, about 86K views when read
- **Play it:** [xikhar.github.io/sumiro](https://xikhar.github.io/sumiro/)
- **Read on:** 2026-11-04

## Verdict

Possible: yes.
The game is real, and it loads and plays.
Feasible for us: yes for the art and game-client side, which an open-source skill now packages with a measured cost of about 6 USD of generation per small game.
The thread covers nothing blockchain-specific.
Cheating, download size and mobile support are the gaps to solve before putting any value on a game made this way.

## The process as posted

Stack: Opus 5.5, Flux 3 Max, GPT Image, Tripo, Blender, Three.js.

1. **Generate a video.** A short clip made with Flux 3 Max on fal becomes the reference for the look, the world and the character.
2. **Build the world.** Take stills from the video, rebuild the assets in Blender, and place them in a Three.js scene.
   Claude Code dynamic workflows run several agents that build and check in parallel.
3. **Make the character.** Take a still of the hero, have GPT Image draw 4 side views, lift those to a 3D model with Tripo, and let Opus add cloth physics and animations.
4. **Test the gameplay.** Play the prototype and confirm it works before building more.
5. **Plan the full world.** GPT Image draws concept art for every level in the established style, up to 8 images per level.
6. **Build every scene, then iterate.** Each concept image becomes a playable 3D level.
   Play it, report bugs, let the agents fix them, and repeat.

From the author's replies: the core mechanics are puzzles, parkour and platforming, with enemies and combat later in the game.
The demo video in the post was recorded by Claude playing the game, which is why the movement looks stiff.

## What the thread leaves out

- **The prompt.** The first post promises a prompt further down the thread, but none was posted.
  The closest public equivalent is the Video2Game skill that the author credits as the inspiration (see below).
- **The author's head start.** The author has at least five earlier AI-built Three.js game repos since August 2026 (a cyberpunk city, a third-person action game, a Sisyphus game, a painterly world, a voxel game) and their own MIT-licensed skill pack for asset creation, `xikhar/atlas`.
  The 24 hours is build time on top of that tooling and practice, not a cold start.
- **Cost.** Several replies asked what it cost, and none got an answer.
- **Source code.** The `sumiro` source is not public.
  Only the built game is, inside `xikhar/xikhar.github.io`.

## What I checked

Tested in Chrome on a Mac on 2026-11-04.

- It loads and plays.
  The boot screen took about 67 s and 55 MB of downloads on this connection before the title screen appeared.
- It holds 60 fps while walking, at 2x pixel density.
- It has real game structure: a menu (New Game, Options, Controls, Credits), chapter title cards, 6 chapters in the code (climb, pass, pines, temple, sea, summit), ledge climbing and shimmying, a combat module and an ink-wash shader.
- There are no audio files in the build, so its 54 KB audio module must synthesize all sound in code.
- The published build is 122 MB in 151 files, and 100 MB of that is 26 GLB models.
  It ships a Draco decoder, yet single models still reach 12 to 14 MB.
  One of the largest files is `test_rocks.glb`, which looks like a leftover test asset.
  The full file list with sizes is in [data/2026-11-04-sumiro-build-files.tsv](data/2026-11-04-sumiro-build-files.tsv).
- Controls are keyboard only, with no touch support.

Replies were mostly praise and unanswered cost questions.
The skeptical ones: one person said the same idea built with Opus 4.8 came out badly, others called it a demo rather than a full game, and one asked for mobile controls.

## Open-source pieces we can reuse

### Video2Game skill (the method behind the thread)

- Repo: [github.com/lovisdotio/video-to-game](https://github.com/lovisdotio/video-to-game), MIT, 446 stars on 2026-11-04, by Lovis Odin ([@OdinLovis](https://x.com/OdinLovis)).
- Gallery: [fal-video-to-game.vercel.app](https://fal-video-to-game.vercel.app), 31 playable games, each a single `index.html` with Three.js and no other library.
- Workflow: generate a 10 to 15 s gameplay video (MiniMax H3 Max on fal), split it into frames and write a spec from them, and generate every asset on fal from those frames (concept sheets, image-to-3D with Meshy, Tripo or Hunyuan 3D, rigging, sound, music).
  Then build the game from a Three.js template, compare game and video side by side at fixed timestamps, and let the agent play the game with the keyboard and film its best seconds.
- Measured cost: the 31 games used 1,013 fal calls (594 images, 194 3D models, 290 sounds and music tracks) for 202 USD in total.
  That is about 6 USD per game, ranging from 0.79 to 15.48 USD.
- Video prompt rules: one original concept with one verb at its heart, the mechanic shown working, a steady playable camera, no HUD or on-screen text, and a strong art direction in a few words.
  Clips are 10 to 15 s at 1080p and 16:9, and the authors generated a few per concept and kept the clearest.
- Install in Claude Code: `claude plugin marketplace add lovisdotio/video-to-game`, then `claude plugin install video-to-game@video-to-game`.

### Atlas (the author's asset skills)

- Repo: [github.com/xikhar/atlas](https://github.com/xikhar/atlas), MIT.
- Skills: `asset-core`, `model3d-gen`, `pbr-texture-gen`, `character-consistency`, `threejs-pipeline` and `threejs-shaders`, plus 2D sprite, tileset, background, animation and UI generators.
- The most useful idea is in `model3d-gen`: treat AI 3D output as raw material.
  Clean it up in headless Blender (decimate, re-pivot, re-unwrap UVs, fix materials) and validate it with `gltf-transform` before it goes into the game.
- Install: `npx skills add xikhar/atlas`.

## Feasibility for us

- **Tools.** We already have `FAL_KEY` and `OPENAI_API_KEY` in the global env, Blender.app, ffmpeg, and Claude Code on Opus 5.5.
  Missing: `pip install fal-client`, and `playwright-core` for the playtest recorder.
  No separate Tripo account is needed, since Tripo runs on fal.
- **Cost.** A small one-level game costs about 5 to 15 USD of fal calls, going by the Video2Game numbers.
  The Sumiro cost was not disclosed.
  For its scale (one video, up to about 50 concept images, a few dozen models), Video2Game's average of about 0.20 USD per call puts it in the tens of dollars; that is my estimate, not a reported figure.
  The larger cost is likely Claude usage, because dynamic workflows run many agents at once.
  Every fal or OpenAI call needs approval first under the spending rules.
- **Time.** A first small game in a day is realistic with Video2Game.
  Sumiro-level polish comes from the play-and-fix loop and from practice, so budget days to weeks for the first one.

## Blockchain fit

What fits well:

- A Three.js game is a plain web page, so wallet libraries (viem and wagmi on EVM, the wallet adapter on Solana) drop straight in, with no engine export to fight.
- Hosting is static.
  GitHub Pages works, as Sumiro shows, and Cloudflare with R2 for the large model files is another option.
- Generated GLB characters and items can serve directly as NFT media (`animation_url`), and the concept-art step keeps a whole collection in one style.

What the workflow does not cover:

1. **Cheating.** All game logic runs in the browser, so any reward paid on a score the client reports can be faked.
   Value needs either server-side verification, such as replaying the recorded inputs with a fixed seed in a Worker, or a design where on-chain value does not depend on claimed skill, such as owned cosmetics or server-judged tournaments.
   Replay checks only work if the simulation is deterministic, which has to be designed in from the start (fixed timestep, seeded randomness).
2. **Size and mobile.** A 122 MB build, a 67 s load and keyboard-only controls do not suit players who arrive from X, Telegram or a wallet's in-app browser on a phone.
   Set a download budget, compress models (meshopt or Draco geometry, KTX2 textures), stream each level, and build touch controls from day one.
3. **Rights.** Check each model's commercial terms on fal before selling anything made with it.
   In the US, art generated purely by AI generally cannot be copyrighted, which weakens the IP behind an NFT collection made only from generated art.
4. **On-chain work.** Contracts, wallet flows and a security review are separate work.
   The `evm-security` and `solidity-security` skills cover the review.
5. **Depth.** The skeptics are right that this is a polished vertical slice, not a long game.
   For a blockchain game that can be enough if the loop is short and replayable, such as seasons or tournaments.

## Rechecked on 2026-11-07

- The post had about 5.9 million views, up from about 86K when first read; the thread itself is unchanged and still has no prompt.
- The published build grew to 128 MB in 151 files (105 MB of it in 26 GLB models), and the source is still not public; the build carries no licence.
- In Chrome on the same Mac the title screen appeared after about 35 s and 57 MB of downloads, and walking held 60 fps.
- The controls are still keyboard only, and the game has no score, so nothing in it could be checked by a server.
- Our answer to this thread so far is [Dockstack](../calibration/2026-11-06-video2game/README.md): a 2.5 MB build that loads in about half a second, works on phones, and has a score a server can replay.

## Possible next step

Install Video2Game, pick one concept with a clear on-chain hook, and build a single-level game for roughly 5 to 15 USD of fal calls (needs approval).
Then measure load size and mobile play, and add wallet connect plus a testnet contract.
Tracked in [issue #1](https://github.com/imDev2023/x-gaming/issues/1).
