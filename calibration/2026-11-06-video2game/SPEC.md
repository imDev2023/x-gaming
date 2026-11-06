# Dockstack: spec from the video

Written from [take 1](video/take1.mp4) before any game code, following the Video2Game skill's `study-the-video.md`.
Frame numbers are `study/f_NNN.jpg`, one every 0.5 s, so `f_015` is at 7.0 s.

## Prompt

> Cozy low-poly 3D game, flat-shaded, warm dusk harbour: a small dock crane swings light tan wooden cargo crates with diagonal braces and dark metal corners out over a rocking barge and drops them one by one; the stack grows taller and sways with the waves, and a misplaced crate tumbles into the water with a splash. Steady side-on camera.

MiniMax H3 Max, 10 s, 1080p, seed 101; the clip came back 10.14 s long with no cuts.

## Camera

- Side-on, at about deck height plus 2 m, looking slightly up at the stack; a long, flat lens with almost no distortion (`f_001`, `f_015`).
- The stack sits a little left of centre; the crane's portal fills the left fifth of the frame and the wheelhouse the right third (`f_015`).
- One slow move: the camera drifts right and slightly in over the 10 s, keeping the stack framed (`f_001` to `f_020`).
- A crate is about 75 px tall in a 540 px frame, so the frame shows about 7 m of height at the stack.

## Hero

There is no character: the player is the crane.
The readable part at small size is the hook: an orange hook block (`#b16713`) on a dark rope, with a 4-point rope sling holding the crate (`f_001`, `f_007`).

## The mechanic: stack

- The crane brings a crate over the boat on its sling, the crate drops onto the stack, and the stack grows into a stepped pyramid about 4 crates wide and 4 high (`f_001` to `f_016`).
- Feedback in the video: crates settle with a small bump, the stack shifts with the boat's slow roll.
- The key moment: a misplaced crate tips off the side of the stack, tumbles into the water and throws a white splash ring (`f_018` to `f_020`, 8.5 to 10 s).

## World

- Left: a concrete quay with bollards, street lamps, stacked crates, pallets and a plank pile, a red-brick terraced house, and the crane standing on the quay edge (`f_001`).
- Centre: the boat, bow to the left, with a dark low hull, a row of tyre fenders, and an open cargo deck where the stack grows (`f_015`).
- Right: a tug-style wheelhouse with a red roof edge, square windows, a life ring, a mast with radar domes and rigging, and a red funnel with a dark top (`f_015`, `f_020`).
- Behind: warm haze, a low town silhouette, and big soft cumulus clouds (`f_001`, `f_020`).
- Scale cues: crates are 1 m, the wheelhouse door is about 2 m, the quay stands about 1.5 m above the water.

## Look

Measured from the frames with an 8 x 8 px average; the strong warm grade means a surface that reads as white measures as tan.

| Part | Hex | Frame |
| --- | --- | --- |
| Sky, high | `#d4a98a` | f_015 |
| Sky, middle | `#e3b68b` | f_015 |
| Cloud | `#efd29c` | f_015 |
| Sun haze at the horizon | `#f0bd74` | f_015 |
| Water, near | `#2f281e` | f_020 |
| Water, far (reflects the haze) | `#e5c184` | f_020 |
| Splash and foam | `#c1b47e` | f_020 |
| Hull | `#2e2216` | f_015 |
| Wheelhouse wall (reads as white) | `#ae8662` | f_015 |
| Roof edge and funnel red | `#97331e`, `#83311c` | f_015 |
| Crate wood, lit | `#9c5d2a` | f_015 |
| Crate wood, shaded | `#734828` | f_015 |
| Crane steel | `#423324` | f_001 |
| Crane cab yellow | `#af7127` | f_001 |
| Quay concrete | `#5f4730` | f_001 |
| Brick | `#d46f3a` | f_001 |
| Hook block | `#b16713` | f_015 |

- Light: a low sun behind and left of the boat, inside the haze, so surfaces facing the camera are in soft warm shade and edges catch a rim of light.
- Materials: flat low-poly with soft gradients, no visible texture detail beyond wood boards and brick courses.
- Atmosphere: thick warm haze that swallows the town; no fog near the stack.
- Grade: warm gain (red over green over blue, about 1 : 0.78 : 0.58 on neutral surfaces), lifted blacks, a soft vignette.
  In the build the warmth comes from warm lights on neutral materials plus a mild grade, not from a strong post grade: the generated sky plate already carries the video's grade, and grading it again would double it.

## Players

One.

## Game design

The video is 10 s of stacking; the game makes it a shipment to load.

- **Controls:** one action, release the crate: Space, a click or a tap anywhere, gamepad A.
  Enter or the action starts; R or the action restarts at the end.
- **Loop:** the hook brings a crate in from the quay and sweeps it back and forth over the deck; the player releases it; it falls straight down onto the deck or the stack.
  The boat surges and heaves on the swell, so the target moves under the hook.
- **Rules:** a crate rests if its centre lies over what it lands on; otherwise it tips off the side and is lost, splashing into the water like the video's key moment.
  A crate that misses the deck falls between the quay and the hull and is lost the same way.
- **Goal and end:** a shipment of 15 crates, shown as a row of 15 small squares in the top-left corner that fill in as each crate is loaded or lost.
  A pile on the quay was the first plan, but the video's framing leaves no room for 15 crates there.
  When the last crate is down, the boat sounds its horn and sails off to the right; the end line gives crates loaded and stack height, and the action restarts.
- **Progression:** the sweep gets faster with each crate, and the shipment mixes 1 m crates, half-height crates, 2 m long crates and lid boxes, so higher layers need more precise drops.
- **Score:** crates loaded, then stack height as the tie-break.

### Determinism, for the on-chain hook

The on-chain hook is a daily challenge whose scores a server checks by replaying each run, so the simulation is written for exact replay from the start.

- The simulation (`game/sim.js`) uses integers only: positions in micrometres, time in ticks of 1/60 s, gravity as an integer per tick squared.
  No `Math.sin`, no floating point and no wall-clock time reach it, so the same inputs give the same result in any JavaScript engine.
- Randomness (the crate sequence, swell phases) comes from a seeded 32-bit generator; the seed will come from a block hash.
- A run is fully described by its seed and the list of ticks at which the player released a crate.
  `replay(seed, releases)` returns the score, which is what the server will compute.
- Rendering only reads the simulation; roll, tumbling and splashes are visual and never feed back into it.
