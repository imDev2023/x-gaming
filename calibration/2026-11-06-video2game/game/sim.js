// Dockstack simulation: the whole game's rules, in integers only.
//
// Positions are micrometres, time is ticks of 1/60 s, and every operation is integer
// addition, multiplication or floor division of values below 2^53, which IEEE 754
// doubles compute exactly in every JavaScript engine. There is no Math.sin, no floating
// point state and no wall-clock time, so a run replays to the same score anywhere:
// `replay(seed, releases)` is what a server runs to check a claimed score before it
// reaches an on-chain leaderboard.
//
// Rendering only reads this state. Roll, tumbling and splashes are drawn from it and
// never feed back into it.

export const TICK_HZ = 60;
export const UM = 1_000_000; // micrometres per metre

// The crate kit (calibration/2026-11-06-kit), seen side-on: width along X and height.
// `weight` is the piece's share of a shipment, out of 100.
export const CRATES = {
  crate: { w: 1_000_000, h: 1_000_000, weight: 40 },
  half: { w: 1_000_000, h: 500_000, weight: 20 },
  long: { w: 2_000_000, h: 1_000_000, weight: 15 },
  lid: { w: 1_000_000, h: 500_000, weight: 15 },
  planks: { w: 2_000_000, h: 500_000, weight: 10 },
};
const TYPES = Object.keys(CRATES);

// Boat_01's cargo deck, in the boat's frame (briefs.md): flat at 1.0 m above the
// waterline from the bow's knuckle to the wheelhouse.
export const DECK = { left: -5_400_000, right: 2_200_000, y: 1_000_000 };
// The hook's sweep in the world: past the bow on the left, so a careless drop misses
// the boat, and short of the wheelhouse on the right, so a 2 m crate always clears it.
export const HOOK = { left: -6_400_000, right: 1_200_000 };

export const SHIPMENT = 15;
export const G = 2725; // 9.81 m/s^2 in micrometres per tick^2
export const HANG = 1_600_000; // a swinging crate's bottom above the stack's top
export const RELOAD = 54; // ticks for the hook to fetch the next crate
export const DEPART = 240; // ticks of the boat sailing off at the end
export const SWING_MAX = 720; // an unreleased crate drops by itself after 12 s
export const WAVE = 1_000_000; // full scale of wave() and sweep fractions
const SURGE = 220_000; // the boat's surge amplitude along X
const HEAVE = 60_000; // and its heave amplitude

const LIMIT = 2 ** 53;

/** Floor division of integers, checked to stay in the range doubles compute exactly. */
export function idiv(a, b) {
  if (!(Math.abs(a) < LIMIT && b > 0 && Number.isInteger(a) && Number.isInteger(b))) {
    throw new RangeError(`idiv out of exact range: ${a} / ${b}`);
  }
  return Math.floor(a / b);
}

/** mulberry32: a seeded 32-bit generator built from integer operations only. */
export function rng(seed) {
  let a = seed >>> 0;
  return function next() {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), a | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return (t ^ (t >>> 14)) >>> 0;
  };
}

/** A smooth back-and-forth from 0 to WAVE and back over 2 * half ticks (smoothstep ease). */
export function sweep(t, half) {
  const p = ((t % (2 * half)) + 2 * half) % (2 * half);
  const u = p < half ? p : 2 * half - p;
  return idiv(u * u * (3 * half - 2 * u) * WAVE, half * half * half);
}

/** The same motion centred on zero, from -WAVE to WAVE. */
export function wave(t, half) {
  return 2 * sweep(t, half) - WAVE;
}

/** Start a run: the shipment's crate order and the swell come from the seed alone. */
export function createRun(seed) {
  const next = rng(seed);
  const queue = [];
  for (let i = 0; i < SHIPMENT; i++) {
    let roll = next() % 100;
    let type = TYPES[0];
    for (const t of TYPES) {
      if (roll < CRATES[t].weight) { type = t; break; }
      roll -= CRATES[t].weight;
    }
    queue.push(type);
  }
  const s = {
    seed: seed >>> 0,
    tick: 0,
    phase: 'swing',
    phaseTick: 0,
    index: 0,
    queue,
    swell: {
      surgeHalf: 150 + (next() % 61),
      surgePhase: next() % 400,
      heaveHalf: 100 + (next() % 41),
      heavePhase: next() % 400,
    },
    boatX: 0,
    boatY: 0,
    hookX: HOOK.left,
    hookY: 0,
    hookFrom: HOOK.left,
    crate: null,
    stack: [],
    lost: [],
    releases: [],
    placed: 0,
    events: [],
  };
  moveBoat(s);
  startSwing(s);
  return s;
}

function moveBoat(s) {
  const w = s.swell;
  s.boatX = idiv(SURGE * wave(s.tick + w.surgePhase, w.surgeHalf), WAVE);
  s.boatY = idiv(HEAVE * wave(s.tick + w.heavePhase, w.heaveHalf), WAVE);
}

/** The stack's highest top, relative to the deck. */
export function stackTop(s) {
  let top = 0;
  for (const c of s.stack) if (c.top > top) top = c.top;
  return top;
}

/** Ticks for one sweep across: the hook speeds up with each crate. */
export function swingHalf(index) {
  return Math.max(56, 112 - 4 * index);
}

/** Where the hook is `phaseTick` ticks into crate `index`'s swing. */
export function hookAt(index, phaseTick) {
  return HOOK.left + idiv((HOOK.right - HOOK.left) * sweep(phaseTick, swingHalf(index)), WAVE);
}

function startSwing(s) {
  const type = s.queue[s.index];
  s.phase = 'swing';
  s.phaseTick = 0;
  s.hookX = HOOK.left;
  // The crane does not bob: the crate hangs HANG above the stack's top at rest.
  const bottom = DECK.y + stackTop(s) + HANG;
  s.crate = { type, x: s.hookX, y: bottom, v: 0 };
  s.hookY = bottom + CRATES[type].h;
}

/** What a crate with footprint [l, r] would land on: the highest top below `maxTop`. */
function supportUnder(s, l, r, maxTop) {
  const under = [];
  if (r > DECK.left && l < DECK.right) under.push({ l: DECK.left, r: DECK.right, top: 0 });
  for (const c of s.stack) {
    const cl = c.x - idiv(CRATES[c.type].w, 2);
    const cr = cl + CRATES[c.type].w;
    if (r > cl && l < cr) under.push({ l: cl, r: cr, top: c.top });
  }
  let top = -1;
  for (const u of under) if (u.top <= maxTop && u.top > top) top = u.top;
  if (top < 0) return null;
  const at = under.filter((u) => u.top === top);
  return { top, lo: Math.max(l, Math.min(...at.map((u) => u.l))), hi: Math.min(r, Math.max(...at.map((u) => u.r))) };
}

/** Land or lose the falling crate this tick, if it reaches something. */
function fall(s) {
  const c = s.crate;
  const def = CRATES[c.type];
  const deckWorld = DECK.y + s.boatY;
  const prev = c.y;
  c.v += G;
  c.y -= c.v;
  const rel = c.x - s.boatX;
  const l = rel - idiv(def.w, 2);
  const r = l + def.w;
  // Only tops the crate was still above last tick: it cannot land on a column beside it.
  const sup = supportUnder(s, l, r, prev - deckWorld);
  if (sup && c.y <= deckWorld + sup.top) {
    if (rel < sup.lo || rel > sup.hi) {
      const side = rel < sup.lo ? -1 : 1;
      s.lost.push({ type: c.type, x: rel, bottom: sup.top, reason: 'tip', side, edge: side < 0 ? sup.lo : sup.hi, tick: s.tick });
      s.events.push({ type: 'tip', side, x: rel, bottom: sup.top });
    } else {
      const entry = { type: c.type, x: rel, bottom: sup.top, top: sup.top + def.h, tick: s.tick };
      s.stack.push(entry);
      s.placed += 1;
      const margin = Math.min(rel - sup.lo, sup.hi - rel);
      s.events.push({ type: 'land', on: sup.top === 0 ? 'deck' : 'crate', x: rel, bottom: sup.top, wobble: margin * 10 < def.w });
    }
    endDrop(s);
  } else if (!sup && c.y < deckWorld - UM) {
    s.lost.push({ type: c.type, x: rel, bottom: -UM, reason: 'miss', side: rel < 0 ? -1 : 1, tick: s.tick });
    s.events.push({ type: 'miss', x: c.x });
    endDrop(s);
  }
}

function endDrop(s) {
  s.crate = null;
  s.phase = 'settle';
  s.phaseTick = 0;
  s.hookFrom = s.hookX;
}

/**
 * Advance one tick. `press` is whether the release button was pressed since the last
 * tick; it only counts while a crate swings. Returns this tick's events.
 */
export function step(s, press) {
  s.tick += 1;
  s.phaseTick += 1;
  s.events = [];
  moveBoat(s);
  if (s.phase === 'swing') {
    s.hookX = hookAt(s.index, s.phaseTick);
    s.crate.x = s.hookX;
    if (press || s.phaseTick >= SWING_MAX) {
      if (press) s.releases.push(s.tick);
      s.phase = 'fall';
      s.phaseTick = 0;
      s.events.push({ type: 'release', x: s.hookX, auto: !press });
    }
  } else if (s.phase === 'fall') {
    fall(s);
  } else if (s.phase === 'settle') {
    // The hook goes back to the quay for the next crate.
    s.hookX = s.hookFrom + idiv((HOOK.left - s.hookFrom) * sweep(s.phaseTick, RELOAD), WAVE);
    if (s.phaseTick >= RELOAD) {
      s.index += 1;
      if (s.index >= SHIPMENT) {
        s.phase = 'depart';
        s.phaseTick = 0;
        s.events.push({ type: 'depart' });
      } else {
        startSwing(s);
        s.events.push({ type: 'next', crate: s.crate.type });
      }
    }
  } else if (s.phase === 'depart' && s.phaseTick >= DEPART) {
    s.phase = 'done';
    s.events.push({ type: 'done', score: score(s) });
  }
  return s.events;
}

/** Crates loaded first, then the stack's height in centimetres. */
export function score(s) {
  return s.placed * 1000 + idiv(stackTop(s), 10_000);
}

/** A short fingerprint of the full state, for determinism tests. */
export function hash(s) {
  const text = JSON.stringify([s.tick, s.phase, s.index, s.boatX, s.boatY, s.hookX, s.crate, s.stack, s.lost, s.releases]);
  let h = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) h = Math.imul(h ^ text.charCodeAt(i), 0x01000193) >>> 0;
  return h.toString(16).padStart(8, '0');
}

/**
 * Replay a run from its seed and the ticks at which the player released a crate, as a
 * server would. Rejects a release that could not have happened.
 */
export function replay(seed, releases, maxTicks = SHIPMENT * (SWING_MAX + 200) + DEPART + 10) {
  const s = createRun(seed);
  const want = new Set(releases);
  if (want.size !== releases.length) return { ok: false, reason: 'duplicate release tick' };
  while (s.phase !== 'done' && s.tick < maxTicks) {
    const press = want.has(s.tick + 1);
    if (press && s.phase !== 'swing') return { ok: false, reason: `release at tick ${s.tick + 1} while ${s.phase}` };
    step(s, press);
  }
  if (s.phase !== 'done') return { ok: false, reason: 'run did not finish' };
  return { ok: true, score: score(s), placed: s.placed, lost: s.lost.length, height: stackTop(s), ticks: s.tick, hash: hash(s) };
}
