// Tests for the Dockstack simulation: node --test game/
import test from 'node:test';
import assert from 'node:assert/strict';
import {
  createRun, step, replay, score, hash, stackTop, sweep, rng, hookAt,
  CRATES, DECK, HOOK, SHIPMENT, SWING_MAX, UM, WAVE,
} from './sim.js';

/**
 * Whether to press now so the crate releases over `target` in the boat's frame: the
 * press takes effect next tick, so release at the tick where the hook is closest.
 */
function closest(s, target) {
  if (s.phase !== 'swing') return false;
  const d1 = Math.abs(hookAt(s.index, s.phaseTick + 1) - s.boatX - target);
  const d2 = Math.abs(hookAt(s.index, s.phaseTick + 2) - s.boatX - target);
  return d1 <= d2 && d1 < 150_000;
}

/** A simple player: release when the hook is over `target(s)` in the boat's frame. */
function play(seed, target) {
  const s = createRun(seed);
  while (s.phase !== 'done') step(s, s.phase === 'swing' && closest(s, target(s)));
  return s;
}

/** Aim for the left end of the stack's lowest stable spot: fills a row, then the next. */
function lowestSpot(s) {
  const w = CRATES[s.crate.type].w;
  let best = null;
  for (let x = DECK.left + w / 2 + 100_000; x <= DECK.right - w / 2 - 300_000; x += 250_000) {
    let top = 0;
    for (const c of s.stack) {
      const half = CRATES[c.type].w / 2;
      if (x + w / 2 > c.x - half && x - w / 2 < c.x + half) top = Math.max(top, c.top);
    }
    if (!best || top < best.top) best = { x, top };
  }
  return best.x;
}

test('the same seed and inputs give the same run', () => {
  const a = play(7, lowestSpot);
  const b = play(7, lowestSpot);
  assert.equal(hash(a), hash(b));
  assert.equal(score(a), score(b));
  assert.equal(a.phase, 'done');
});

test('a server replay of a live run gives the same score and state', () => {
  for (const seed of [1, 7, 20261106, 4_000_000_000]) {
    const live = play(seed, lowestSpot);
    const r = replay(seed, live.releases);
    assert.equal(r.ok, true, r.reason);
    assert.equal(r.score, score(live));
    assert.equal(r.hash, hash(live));
    assert.equal(r.placed + r.lost, SHIPMENT);
  }
});

test('different seeds give different shipments', () => {
  const orders = new Set([1, 2, 3, 4, 5].map((seed) => createRun(seed).queue.join(',')));
  assert.ok(orders.size >= 4);
});

test('every number in the state stays an integer', () => {
  const s = createRun(11);
  const ints = (v) => (typeof v === 'number' ? Number.isInteger(v) : v && typeof v === 'object' ? Object.values(v).every(ints) : true);
  while (s.phase !== 'done') {
    step(s, s.phase === 'swing' && s.phaseTick === 40);
    assert.ok(ints(s), `non-integer state at tick ${s.tick}`);
  }
});

test('a crate centred over the deck rests on it', () => {
  const s = play(3, () => -2_000_000);
  assert.ok(s.stack.length > 0);
  const first = s.stack[0];
  assert.equal(first.bottom, 0);
  assert.ok(Math.abs(first.x + 2_000_000) < 400_000);
});

test('a crate dropped past the bow misses the boat', () => {
  const s = createRun(5);
  s.queue = Array(SHIPMENT).fill('crate');
  s.crate.type = 'crate';
  // Release on the first tick, while the hook is still at the far left of its sweep.
  const events = step(s, true);
  assert.equal(events[0].type, 'release');
  while (s.phase === 'fall') step(s, false);
  assert.equal(s.lost.length, 1);
  assert.equal(s.lost[0].reason, 'miss');
});

test('a crate whose centre is past its support tips off', () => {
  const s = createRun(9);
  s.queue = Array(SHIPMENT).fill('crate');
  s.crate.type = 'crate';
  // One crate on the deck at x = -2 m; aim the next so its centre overhangs that crate's
  // right edge (-1.5 m) by 0.2 m, with the deck's surface 1 m below.
  s.stack.push({ type: 'crate', x: -2_000_000, bottom: 0, top: UM, tick: 0 });
  s.crate.y = DECK.y + UM + 1_600_000;
  while (s.phase === 'swing') step(s, closest(s, -1_300_000));
  while (s.phase === 'fall') step(s, false);
  // It overhangs the crate below and the deck is lower, so it lands on the crate's top and tips.
  assert.equal(s.lost.length, 1);
  assert.equal(s.lost[0].reason, 'tip');
  assert.equal(s.lost[0].side, 1);
});

test('replay rejects a release that could not happen', () => {
  const live = play(2, lowestSpot);
  // A second release 3 ticks after the first, while that crate is still falling.
  const r = replay(2, [live.releases[0], live.releases[0] + 3]);
  assert.equal(r.ok, false);
  assert.match(r.reason, /while fall/);
  assert.equal(replay(2, [live.releases[0], live.releases[0]]).ok, false);
});

test('an unreleased crate drops by itself after the swing limit', () => {
  const s = createRun(4);
  let ticks = 0;
  while (s.phase === 'swing') { step(s, false); ticks += 1; }
  assert.equal(ticks, SWING_MAX);
  assert.equal(s.releases.length, 0);
});

test('the hook sweeps across its whole range', () => {
  assert.equal(sweep(0, 100), 0);
  assert.equal(sweep(100, 100), WAVE);
  assert.equal(sweep(200, 100), 0);
  assert.equal(sweep(50, 100), WAVE / 2);
  const s = createRun(1);
  let min = Infinity, max = -Infinity;
  for (let i = 0; i < 400 && s.phase === 'swing'; i++) {
    step(s, false);
    min = Math.min(min, s.hookX); max = Math.max(max, s.hookX);
  }
  assert.equal(min, HOOK.left);
  assert.equal(max, HOOK.right);
});

test('the generator matches the reference mulberry32', () => {
  // The published reference implementation, which returns a float in [0, 1).
  function reference(a) {
    return function () {
      let t = (a += 0x6d2b79f5);
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  for (const seed of [1, 42, 20261106]) {
    const ours = rng(seed);
    const ref = reference(seed);
    for (let i = 0; i < 100; i++) assert.equal(ours() / 4294967296, ref());
  }
});

test('score ranks crates loaded first, then height in centimetres', () => {
  const s = createRun(1);
  s.placed = 12;
  s.stack = [{ type: 'crate', x: 0, bottom: 0, top: 4_567_891 }];
  assert.equal(score(s), 12_456);
  assert.equal(stackTop(s), 4_567_891);
});
