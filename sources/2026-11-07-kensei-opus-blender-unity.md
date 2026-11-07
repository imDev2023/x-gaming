# Kensei: Opus 5.5 + Blender + Unity, a 3D game level in 14 steps

- **Source:** [x.com/0xKense1/status/2112557260375298530](https://x.com/0xKense1/status/2112557260375298530) (an X Article)
- **Author:** Kensei ([@0xKense1](https://x.com/0xKense1))
- **Posted:** 2026-10-20, about 49.9K views, 79 likes and 166 bookmarks when read
- **Read on:** 2026-11-07

## Verdict

Useful, and the most practical source so far for the step Lantern River is stuck on: getting from code-built shapes to a look worth sharing.
Its main lesson is a division of labour, not a tool: a generator makes only the few solid hero objects that code cannot make well, from 3 or 4 views each; code builds the architecture with real-size CC0 textures; free CC0 models dress it; and one look-only pass is judged against an approved mood image.
His own first pass looked flat and grey, as ours does, and those three steps fixed it.
Its cleanup recipe holds up: I rebuilt it as a headless script for our Blender 4.3, and its claim that a diffuse bake turns metal black reproduced in our Three.js check page.
It is a Unity desktop game with 70,000 to 80,000-triangle models, so the budgets and the engine half do not carry over to a phone browser game; there is no demo, repo or build size.

## What the article says

The level is a kitchen at 40 times real size, where a 4 cm inventor with a shrink ray crosses the counter past a house cat as the boss; it took 2 days and 31 Claude Code sessions.

- **Pick a game that suits generated 3D.** Generators do well at solid hero objects and badly at thin loose detail (hair, cloth, long grass), so he chose an idea with a few strong objects and a lot of space around them, and wrote the whole game on one page that every brief points at.
- **A generator only makes what code cannot.** Anything with a simple shape (walls, cabinets, a sugar cube, toast, a rope) is a Blender script; Poly Haven's CC0 models and textures fill the rest.
- **Bill:** 16 Tripo models for 8.20 USD (60 credits, 0.60 USD, with detailed geometry; 40 credits for standard); 52 Poly Haven models, 35 props made in code, every rig and animation for nothing; 31 sessions worth about 88 USD at list prices, paid through a subscription.
- **Reference images first.** Two or three mood pictures until the look is right, then a turnaround sheet per character made from the approved picture: front, sides and back on white, even light, A-pose, hands open and empty.
  His first heroine was drawn holding the ray and the generator welded it to her hand, so the ray got a sheet of its own.
  Views are labelled by what they show, since sheets often swap left and right; props go 8 to a sheet, separated, in 3/4 view.
- **3 or 4 views, not one.** From one front image the cat came back with a second tail; from three views it matched the sheet.
  He calls Tripo's API v3 directly (`multiview-to-model`, model `v3.1-20260211`, PBR, detailed geometry and texture), polls the task, and logs the credit balance before and after every call.
- **Make each model light enough.** Tripo models arrive at about 2 million triangles; a headless Blender script decimates a copy, bakes the high detail into a normal map, bakes the colour as emission (a diffuse bake turns metal black) and keeps the original roughness and metal map.
  The cat went from 1,974,649 to 80,000 triangles in 95 s; the heroine 70,000, the toaster and ray 30,000, the spoon 12,000.
- **Rigs and animation in code, for free.** A humanoid armature placed from measured joints with Mixamo bone names maps itself in Unity's Humanoid importer; the cat got 28 bones and four clips keyframed by script.
  Traps: vertices with no bone trail behind (the whiskers), Blender 5's FBX exporter drops animations unless they are NLA strips, and stacked tilts point the head at the sky.
- **The room as code**, built at real size in centimetres and scaled, with CC0 textures mapped at real size so a plank still reads as a plank, and empty markers where each generated prop goes.
- **Dressing rules:** clusters of 3 to 7 items at varied heights rather than rows, slight random turns, real-world logic (fruit in the bowl, cups by the kettle), big items at the back, the hero's route kept clear, colliders only where the hero can touch; then a raycast snaps every item onto the surface below it and every item moved by more than 1 cm is listed.
  The snap came from a cup that hovered above its saucer.
- **One look-only brief** fixed the flat grey first build against the mood picture: tilt-shift depth of field, reflection probes on wet stone, a cool moon key against warm pools, ambient occlusion, ACES, bloom, grain and split toning, with before and after shots from the same spot and the frame rate before and after.
- **Look, then measure.** The bugs that mattered were found by numbers, not screenshots: a spoon bridge floating 2.8 m above the counter, a towel bulging 1.2 m out of its plane, a crumb placed higher than the hero can jump.
  Every brief asks for a screenshot and the numbers next to it.
- **Unity through its official agent plugin**, installed per project because each of its 30-odd skills loads into every session, with git and LFS from the first prompt and a commit before every brief.
- **One short brief per system, each in a fresh session**, all starting with the same header (what the game is, what already works, do one task, never delete files, stop after two failures, append at most 15 lines to a progress file).
  Opus 5.5 took geometry and art direction (17 sessions, 70 USD); Sonnet 5.5 took clear checkable jobs (14 sessions, 17 USD).
  A shell loop runs the briefs in a row and, when a session hits the usage limit, waits for the reset and restarts the same brief with a note to continue.
- **He plays; the agent fixes.** A full agent playthrough found real blockers but was slow and among the dearest sessions, so he stopped it.
  A free open-source generator on an 8 GB laptop GPU gave soft faces and fused hands.

## What the article leaves out

- **A way to check it.** No playable demo, no repo, no build size and no frame rate on any device; the author asks readers whether to release a demo.
- **Phones and the web.** It is Unity on a desktop with URP effects (depth of field, ambient occlusion, reflection probes) and 70,000 to 80,000-triangle hero models, several times a phone browser's budget.
- **Real spend.** The 88 USD of sessions is a list-price estimate of subscription use; only the Tripo bill is money paid.
- **Rights.** Nothing on Tripo's output terms or the licence of the Starter Assets animations.
- **Score or replay.** It is a single-player level with no score, so nothing on determinism.

## What I checked

Checked on 2026-11-07.

- **The thread.** Read in full in the owner's Chrome, which was signed in to X this time; the page's text tool cut every paragraph short, so the full text and code blocks came from the free fxtwitter API.
  The 9 replies loaded as 3 unrelated promotional posts from other accounts and none from the author.
- **The bake recipe, rebuilt and run.** [Lantern River's `tools/lowpoly_bake.py`](https://github.com/imDev2023/lantern-river/blob/main/tools/lowpoly_bake.py) does the same job headless in our Blender 4.3, with one change: it unwraps the low copy afresh and bakes roughness and metal too, so models with several materials and overlapping UVs work as well as a single Tripo atlas.
  - Poly Haven's CC0 `rock_moss_set_01`: 63,127 triangles to 6,000 in 4.5 s, a 828 KB GLB with colour, normal and roughness-metal maps at 1024 px, 481 KB after `gltf-transform optimize` (meshopt, WebP); `gltf-transform validate` found no errors, and at viewing distance it reads like the original.
  - Poly Haven's CC0 `brass_candleholders`, the metal test: 41,936 to 6,000 triangles.
    Baked as emission it kept its brass in our Three.js check page; baked as diffuse colour it rendered black, and the colour map's mean came out at 38% of the emission bake's.
    The claim holds.
- **Tripo on fal.** We have no Tripo key, but fal's model list (free) carries `tripo3d/h3.1/multiview-to-3d`, which matches the article's v3.1 model: 2 to 4 views in the order front, left, back, right, PBR, standard or detailed geometry and texture, a face limit and seeds, at 0.01 USD per credit like the v2.5 endpoints we priced before.
  It also has `tripo3d/p1` and `p2` image-to-3D and a `tripo3d/tripo/remesh` endpoint.
  The credits each option uses on fal are not in the price list, so the 40 and 60-credit figures are the article's.
- **Poly Haven covers our dressing.** Its API lists 521 CC0 models, including mossy rock sets, wooden barrels, crates and buckets, planter boxes, potted plants, moss, a wooden lantern, street lamps and a modular wooden pier.
- **Unity's plugin is real:** [Unity-Technologies/unity-agent-plugin](https://github.com/Unity-Technologies/unity-agent-plugin), created 2026-08-06, about 620 stars, last pushed 2026-11-06.
  We build for the browser in Three.js, so I did not install it.
- **Not checked:** the rigging and animation steps (Lantern River's hero is a boat and needs no rig), Blender 5's FBX trap, and the Unity half.

## What helps us

For Lantern River, whose code-built look the owner rejected on 2026-11-07:

1. **Generate only the hero objects.** The boat, the shrine and the lantern-gate post are solid objects that generators do well and that carry the look; the canal walls, houses, stairs and bridges are simple shapes for code with real-size CC0 plaster, timber, brick and stone textures; rocks and dressing come from Poly Haven.
   That cuts the earlier plan of about 18 generated models to about 5, and puts the money into views per model instead.
2. **Mood stills before sheets.** One or two 9:16 gameplay stills in the concept video's look, approved by the owner, then every sheet edited from them.
3. **Multiview sheets, empty of what the game draws.** Front, left, back and right on a plain background, labelled by what each view shows; the boat without its flame and the shrine without its paper lanterns, since those glow and flicker in code, like his ray kept apart from the hand.
4. **Bake every model to a phone budget** with `tools/lowpoly_bake.py`, then `gltf-transform optimize`.
5. **Dress the streamed chunks by rule:** clusters with real-world logic (barrels by the stairs, planters on sills, lanterns by the shrine), nothing in the open channel, a snap onto the surface below and a list of anything that moved, plus the numbers next to every screenshot.
6. **One look-only pass against the approved mood still**, with the frame rate on a phone before and after.
7. **Keep our cheap scripted pilots** for blockers and balance and leave feel to the owner, as he did after his agent playthrough proved slow and costly.

## Blockchain fit

None directly: the article has no score, chain or tokens.
Indirectly, the split of generated heroes, code and CC0 dressing makes cosmetic skins cheap to add later: a new boat is one 4-view sheet, one generation and one bake, and it changes nothing in the rules the server replays.

## Next step

Take the split, the multiview sheets and the bake tool into Lantern River's art plan, and put the revised plan and budget to the owner with issue #6's open questions.
