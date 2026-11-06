# Briefs: the Crate_01 kit

Filled in from the brief template in [WORKFLOW.md](../../WORKFLOW.md), one per piece, for [issue #3](https://github.com/imDev2023/x-gaming/issues/3).
The owner approved Crate_01's look as the kit's style on 2026-11-06, including the recessed panels at 62% brightness, and chose these five pieces.
Crate_01 itself keeps its own brief, [../2026-11-05-crate/brief.md](../2026-11-05-crate/brief.md), and is rebuilt by the kit's code as the reference piece.

Every piece shares these lines, which are repeated in each brief so that each one stands alone:

- Game and camera: a third-person browser platformer, seen from a chase camera about 4 m away.
- Style: Crate_01's: chunky low-poly, flat colors, wood parts 5 cm proud of recessed parts darkened to 62% with the `Col` color attribute, and metal fittings 1 cm proud of the wood on every face.
- Grid: the footprint is a multiple of 0.5 m.
- Materials: the kit's two, Wood_A and Metal_A, with no textures.
- Budget: at most 500 triangles, the same as Crate_01.

## CrateHalf_01

```text
First, report what is already in the open Blender scene.

Build a half-height supply crate for a third-person browser platformer, seen from a chase camera about 4 m away.
- Size: 1.0 x 1.0 x 0.5 m
- Budget: at most 500 triangles
- Style: Crate_01's frame, caps, braces and 62% recessed panels, at half the height
- Materials: PBR metallic-roughness: Wood_A and Metal_A, shared with Crate_01; no textures
- Names: object CrateHalf_01, materials Wood_A and Metal_A
- Origin: bottom center at Z=0; apply location, rotation and scale
- Export: selected objects only, GLB, +Y up, to crate_half_01.glb

Then look at it in wireframe and Material Preview from several angles and once from the game camera's distance,
report the triangle count and bounds, fix anything that misses the brief, export, and list the file path and any warnings.
Do not stop until every done check passes.
```

## CrateLong_01

```text
First, report what is already in the open Blender scene.

Build a long supply crate for a third-person browser platformer, seen from a chase camera about 4 m away.
- Size: 2.0 x 1.0 x 1.0 m
- Budget: at most 500 triangles
- Style: Crate_01's frame, caps and 62% recessed panels; mid posts split each long side into two braced bays
- Materials: PBR metallic-roughness: Wood_A and Metal_A, shared with Crate_01; no textures
- Names: object CrateLong_01, materials Wood_A and Metal_A
- Origin: bottom center at Z=0; apply location, rotation and scale
- Export: selected objects only, GLB, +Y up, to crate_long_01.glb

Then look at it in wireframe and Material Preview from several angles and once from the game camera's distance,
report the triangle count and bounds, fix anything that misses the brief, export, and list the file path and any warnings.
Do not stop until every done check passes.
```

## Pallet_01

```text
First, report what is already in the open Blender scene.

Build a wooden pallet for a third-person browser platformer, seen from a chase camera about 4 m away.
- Size: 1.0 x 1.0 x 0.15 m
- Budget: at most 500 triangles
- Style: Crate_01's: deck boards at full brightness over a structure shaded at 62%, so the deck gaps read from above; metal corner blocks echo the crate's caps
- Materials: PBR metallic-roughness: Wood_A and Metal_A, shared with Crate_01; no textures
- Names: object Pallet_01, materials Wood_A and Metal_A
- Origin: bottom center at Z=0; apply location, rotation and scale
- Export: selected objects only, GLB, +Y up, to pallet_01.glb

Then look at it in wireframe and Material Preview from several angles and once from the game camera's distance,
report the triangle count and bounds, fix anything that misses the brief, export, and list the file path and any warnings.
Do not stop until every done check passes.
```

## PlankStack_01

```text
First, report what is already in the open Blender scene.

Build a strapped stack of planks for a third-person browser platformer, seen from a chase camera about 4 m away.
- Size: 2.0 x 0.5 x 0.5 m
- Budget: at most 500 triangles
- Style: Crate_01's: planks on bearers and stickers shaded at 62%, two metal straps 1 cm proud; neighbouring planks must read apart face-on
- Materials: PBR metallic-roughness: Wood_A and Metal_A, shared with Crate_01; no textures
- Names: object PlankStack_01, materials Wood_A and Metal_A
- Origin: bottom center at Z=0; apply location, rotation and scale
- Export: selected objects only, GLB, +Y up, to plank_stack_01.glb

Then look at it in wireframe and Material Preview from several angles and once from the game camera's distance,
report the triangle count and bounds, fix anything that misses the brief, export, and list the file path and any warnings.
Do not stop until every done check passes.
```

## LidBox_01

```text
First, report what is already in the open Blender scene.

Build a small lidded box for a third-person browser platformer, seen from a chase camera about 4 m away.
- Size: 1.0 x 0.5 x 0.5 m
- Budget: at most 500 triangles
- Style: Crate_01's frame and 62% recessed panels without braces; a framed lid over a dark seam, metal corner caps, a latch and two hinges
- Materials: PBR metallic-roughness: Wood_A and Metal_A, shared with Crate_01; no textures
- Names: object LidBox_01, materials Wood_A and Metal_A
- Origin: bottom center at Z=0; apply location, rotation and scale
- Export: selected objects only, GLB, +Y up, to lid_box_01.glb

Then look at it in wireframe and Material Preview from several angles and once from the game camera's distance,
report the triangle count and bounds, fix anything that misses the brief, export, and list the file path and any warnings.
Do not stop until every done check passes.
```
