# x-gaming

Ideas, X posts and GitHub repos for building games, especially blockchain games.
Each source is read in full, checked against what it claims, and judged on whether we could use it.
What we learn is merged into [WORKFLOW.md](WORKFLOW.md), our current game-building pipeline.
Next steps are tracked in [Issues](https://github.com/imDev2023/x-gaming/issues).
Hands-on tests of the workflow live in `calibration/`: [Crate_01](calibration/2026-11-05-crate/README.md), one prop taken from a brief to Three.js by a headless script, [Crate_01 through the live bridge](calibration/2026-11-06-crate-bridge/README.md), the same brief driven through MCP for Blender, [the Crate_01 kit](calibration/2026-11-06-kit/README.md), five more props in its style built through the bridge, and [Dockstack](calibration/2026-11-06-video2game/README.md), a one-level stacking game built end to end with the Video2Game skill, with scores a server can replay, live at [dockstack.vercel.app](https://dockstack.vercel.app/), with its code now in [imDev2023/dockstack](https://github.com/imDev2023/dockstack).
The next game, [Lantern River](https://github.com/imDev2023/lantern-river) for [#6](https://github.com/imDev2023/x-gaming/issues/6), steers a lantern boat down a daily river; its rules, replay check and grey-box are built, and its art is next.
On 2026-11-08 the owner chose a character runner next, [Lamplighter](https://github.com/imDev2023/x-gaming/issues/7), on the same canal town's rooftops, starting with samples for the owner to approve.

## Sources

Newest first.

- **2026-11-07**: [Opus 5.5 + Blender + Unity in 14 steps](sources/2026-11-07-kensei-opus-blender-unity.md) by [@0xKense1](https://x.com/0xKense1/status/2112557260375298530), a 2-day Unity level whose 16 Tripo models cost 8.20 USD, with every prompt, setting and failure.
  - Verdict: useful; generate only the hero objects from 3 or 4 views, build the rest in code with CC0 textures and dressing, and bake each model down; its bake recipe reproduced in our Blender, and it now shapes Lantern River's art plan.

- **2026-11-06**: [The AIOriented repos](sources/2026-11-06-chongdashu-aioriented-vgd.md) by [@chongdashu](https://x.com/chongdashu), 22 repos of VibeGameDev skills, game templates and finished games with their build records, mostly members-only.
  - Verdict: useful; no repo replaces our pipeline, but most sharpen a step of it, and Retro del Sol's server shows the replay check our leaderboard needs.
- **2026-11-04**: [Claude Code + Blender](sources/2026-11-04-lummox-claude-code-blender.md) by [@Lummox_eth](https://x.com/Lummox_eth/status/2117215758472073446), a written guide to driving Blender from Claude Code through MCP to make game-ready assets.
  - Verdict: useful; it tightens our Blender step and adds free CC0 assets, though it shows no demo of its own.
- **2026-11-04**: [Sumiro](sources/2026-11-04-xikhar-sumiro.md) by [@xikhar](https://x.com/xikhar/status/2117776295534997818), a 3D ink-wash platformer built in 24 hours with Claude Code, Flux, GPT Image, Tripo, Blender and Three.js.
  - Verdict: possible, and feasible for the game client; the blockchain side is not covered.

## Reusable tools found so far

- [VGD skills](https://github.com/AIOriented/vgd-skills) (VibeGameDev members): 24 agent skills for Blender, Three.js, fal, Meshy, Tripo, Colyseus and the Wavedash and CrazyGames portals; 15 are installed in this project's gitignored `.claude/skills/`, and every member repo is cloned to the gitignored `reference/aioriented/`.
- [Video2Game](https://github.com/lovisdotio/video-to-game) (MIT): a Claude Code skill that turns an AI gameplay video into a Three.js browser game, at about 6 USD of fal calls per game; [Dockstack](calibration/2026-11-06-video2game/README.md) cost us 2.67 USD with the 3D built for free.
- [Atlas](https://github.com/xikhar/atlas) (MIT): asset-creation skills for 3D models, PBR textures, character turnarounds and Three.js scenes.
- [MCP for Blender](https://github.com/ahujasid/mcp-for-blender) (MIT): lets Claude Code drive a live Blender, see the result from several angles, and import Poly Haven, Sketchfab and Poly Pizza assets; works with Blender 3.0 and newer.
- [Blender Lab MCP](https://www.blender.org/lab/mcp-server/) (Blender Foundation): the official Blender MCP server behind Anthropic's Claude Blender connector; needs Blender 5.1 or newer.
- [Poly Haven](https://polyhaven.com/): about 2,400 HDRIs, textures and models, all CC0 and free.
- [`lowpoly_bake.py`](https://github.com/imDev2023/lantern-river/blob/main/tools/lowpoly_bake.py) (ours, MIT-0): cuts a generated or scanned model to a phone budget in headless Blender, baking colour as emission plus normal and roughness-metal maps; from [Kensei's article](sources/2026-11-07-kensei-opus-blender-unity.md).
- [Unity agent plugin](https://github.com/Unity-Technologies/unity-agent-plugin) (Unity Technologies): connects Claude Code to a live Unity editor; for a Unity build, not our Three.js games.
