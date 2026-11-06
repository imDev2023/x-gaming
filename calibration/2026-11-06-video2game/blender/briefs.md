# Briefs: the Dockstack dock set

One brief per piece, from WORKFLOW.md's template, for the pieces the crate kit does not cover.
The sizes were first estimates; after the first build they were set to the measured bounds, which `checks.py` now holds the pieces to.
The game is seen side-on from about 15 m, so the near (-Y in Blender, +Z in Three.js) side carries the detail and the far side stays plain.

Shared for every piece:

- Style: flat low-poly, untextured, the crate kit's construction rules: parts that sit behind others are darkened through the `Col` color attribute, and a part that covers another stands at least 1 cm proud of it on every face.
- Colors: the video's measured colors divided by its warm grade (about 1 : 0.78 : 0.58), because the game puts the warmth back with warm lights; see [SPEC.md](../SPEC.md).
- Materials: PBR metallic-roughness, no textures, single-sided, all non-metallic (painted steel, concrete, rubber), roughness 0.6 to 0.9.
- Transforms: geometry is built around each piece's own origin, which is its pivot in the game; the build places pieces in the dock layout for looks, and the export writes each piece at its origin.
- Export: each piece alone, GLB, +Y up, to `game/assets/models/<name>.glb`.
- Then look in wireframe and Material Preview from several angles and once from the game camera's side view, report triangles and bounds, run the checks, fix, export.

## Crane_01: the portal crane's fixed part

- Build a harbour portal crane's base for the side-on stacking game: a 4-leg portal with X bracing, a slewing house with a yellow cab and a counterweight, and an A-frame on top.
- Size: 4.10 x 3.70 x 7.71 m, from the counterweight to the portal's bogies and up to the A-frame's sheave; the portal is about 3.2 m wide and 4.6 m tall.
- Budget: at most 2,500 triangles.
- Materials: `Steel_A` (dark olive grey), `Paint_Yellow` (the cab), `Glass_A` (cab windows).
- Origin: bottom centre of the portal; the jib's heel hinge sits at (1.5, 0, 5.4) from it.

## CraneJib_01: the luffing jib

- A lattice boom, 12 m from heel hinge to tip, built lying along +X at 0 degrees; the game luffs it about the hinge between about 36 and 80 degrees, so the hook stays level while it sweeps.
- Size: 12.42 x 1.30 x 1.12 m, from the back of the 1.3 m hinge pin to the sheave head; the truss is 1.0 m square at the heel and tapers to 0.5 m at the tip, where the sheave head carries the hoist rope.
- Budget: at most 1,200 triangles.
- Materials: `Steel_A`, `Paint_Yellow` (sheave head).
- Origin: the heel hinge, so a rotation about Y in Blender (Z in Three.js) luffs it; the tip's rope point is at (12.0, 0, -0.35).

## CraneHook_01: the hook block

- An orange hook block with a sheave and a hook below it; the 4-point sling and the hoist rope are drawn by the game as lines.
- Size: 0.40 x 0.28 x 0.87 m; the hook's bowl dips 2 cm below the origin.
- Budget: at most 300 triangles.
- Materials: `Paint_Orange`, `Steel_A` (hook).
- Origin: the hook's tip, where the sling meets it; the hoist rope leaves the top of the block at (0, 0, 0.85).

## Boat_01: the cargo boat

- A small tug-style cargo boat, bow to the left (-X): a dark hull whose sheer rises at the bow, a row of tyre fenders on the near side, a low bulwark round an open cargo deck, and a two-level wheelhouse aft with a red roof edge, square windows, a door and a life ring, a mast with a yard and two radar domes, and a red funnel with a dark top.
- Size: 12.70 x 4.58 x 9.80 m: the hull runs from the bow at x = -6.2 to the transom at 6.5 and is 4.4 m wide, the near fenders stand 0.18 m outside it, and it reaches from the keel at z = -0.8 to the radar dome at 9.0.
- Budget: at most 5,000 triangles.
- Materials: `Hull_A`, `Paint_White`, `Paint_Red`, `Glass_A`, `Rubber_A`, `Steel_A`.
- Deck: the cargo deck's top is flat at z = 1.0 m from x = -5.4, where the bow's sheer starts to rise 0.35 m to the stem, to the wheelhouse front at 2.4; the game's simulation takes -5.4 to 2.2 m as the deck.
- Origin: on the waterline at the hull's centre (x = 0 is 0.5 m aft of the hull's mid-length), the pivot for heave and roll.

## Quay_01: the quay

- A concrete quay edge with a coping stone, bollards, and two street lamps, which the crane stands on.
- Size: 16.01 x 10.02 x 6.18 m: the lamps stand 3.38 m above the quay top, and the wall reaches 1.2 m below the waterline (2.8 m below the top).
- Budget: at most 1,200 triangles.
- Materials: `Concrete_A`, `Steel_A` (bollards, lamp posts), `Glass_A` (lamp heads).
- Origin: the top of the quay's front edge, at the middle of its length along Y; the quay extends to -X.
