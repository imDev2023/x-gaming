# x-gaming

Ideas, X posts and GitHub repos for building games, especially blockchain games.
Each source is read in full, checked against what it claims, and judged on whether we could use it.
What we learn is merged into [WORKFLOW.md](WORKFLOW.md), our current game-building pipeline.
Next steps are tracked in [Issues](https://github.com/imDev2023/x-gaming/issues).
Hands-on tests of the workflow live in `calibration/`, starting with [Crate_01](calibration/2026-11-05-crate/README.md), one prop taken from a brief to Three.js.

## Sources

Newest first.

- **2026-11-04**: [Claude Code + Blender](sources/2026-11-04-lummox-claude-code-blender.md) by [@Lummox_eth](https://x.com/Lummox_eth/status/2117215758472073446), a written guide to driving Blender from Claude Code through MCP to make game-ready assets.
  - Verdict: useful; it tightens our Blender step and adds free CC0 assets, though it shows no demo of its own.
- **2026-11-04**: [Sumiro](sources/2026-11-04-xikhar-sumiro.md) by [@xikhar](https://x.com/xikhar/status/2117776295534997818), a 3D ink-wash platformer built in 24 hours with Claude Code, Flux, GPT Image, Tripo, Blender and Three.js.
  - Verdict: possible, and feasible for the game client; the blockchain side is not covered.

## Reusable tools found so far

- [Video2Game](https://github.com/lovisdotio/video-to-game) (MIT): a Claude Code skill that turns an AI gameplay video into a Three.js browser game, at about 6 USD of fal calls per game.
- [Atlas](https://github.com/xikhar/atlas) (MIT): asset-creation skills for 3D models, PBR textures, character turnarounds and Three.js scenes.
- [MCP for Blender](https://github.com/ahujasid/mcp-for-blender) (MIT): lets Claude Code drive a live Blender, see the result from several angles, and import Poly Haven, Sketchfab and Poly Pizza assets; works with Blender 3.0 and newer.
- [Blender Lab MCP](https://www.blender.org/lab/mcp-server/) (Blender Foundation): the official Blender MCP server behind Anthropic's Claude Blender connector; needs Blender 5.1 or newer.
- [Poly Haven](https://polyhaven.com/): about 2,400 HDRIs, textures and models, all CC0 and free.
