// Playtest scenario for the Video2Game skill's record_play.mjs:
//   node record_play.mjs "http://127.0.0.1:8000/?autostart" play.mjs -o take.mp4 --seconds 46
//
// Plays Dockstack like a good player, with the Space key only, reading what a player
// sees through window.__game.state. It builds a stepped pyramid as in the video, and
// misplaces the third crate past the bow on purpose, so the video's key moment (a
// crate tumbling into the water) comes early in the take.

const MISPLACE = 2; // index of the crate dropped past the bow
const FALL_TICKS = 34; // a crate falls about 34 ticks from its hang height

/** What a crate of width w centred at x would land on, in the boat's frame. */
function support(s, x, w) {
  const l = x - w / 2, r = x + w / 2;
  const under = [];
  if (r > s.deck[0] && l < s.deck[1]) under.push({ l: s.deck[0], r: s.deck[1], top: 0 });
  for (const c of s.stack) if (r > c.x - c.w / 2 && l < c.x + c.w / 2) under.push({ l: c.x - c.w / 2, r: c.x + c.w / 2, top: c.top });
  if (!under.length) return null;
  const top = Math.max(...under.map((u) => u.top));
  const at = under.filter((u) => u.top === top);
  return { top, lo: Math.max(l, Math.min(...at.map((u) => u.l))), hi: Math.min(r, Math.max(...at.map((u) => u.r))) };
}

/** The lowest well-supported spot between the bow and the middle of the deck. */
function spot(s) {
  let best = null;
  for (let x = -4.6 + s.crateW / 2; x <= 0.6 - s.crateW / 2 + 1e-9; x += 0.05) {
    const sup = support(s, x, s.crateW);
    if (!sup || x < sup.lo + 0.3 || x > sup.hi - 0.3) continue;
    const cost = sup.top * 10 + Math.abs(x + 2.0) * 0.1;
    if (!best || cost < best.cost) best = { x, cost };
  }
  return best ? best.x : -2.0;
}

export async function play(page, { seconds, t0 }) {
  const k = page.keyboard;
  const state = () => page.evaluate(() => window.__game?.state);
  const end = t0 + seconds * 1000 - 150;
  let s = await state();
  if (s?.phase === 'title') await k.press('Space');
  let target = null, forIndex = -1, lastBoat = null, lastTick = 0, boatV = 0;
  while (Date.now() < end) {
    s = await state();
    if (!s || s.phase === 'done') break;
    if (lastBoat !== null && s.tick > lastTick) boatV = (s.boatX - lastBoat) / (s.tick - lastTick);
    lastBoat = s.boatX; lastTick = s.tick;
    if (s.phase === 'swing') {
      if (forIndex !== s.index) { target = s.index === MISPLACE ? -5.7 : spot(s); forIndex = s.index; }
      // Lead the boat: it keeps surging while the crate falls.
      const boatAtLanding = s.boatX + boatV * FALL_TICKS;
      const e1 = Math.abs(s.nextHookX - boatAtLanding - target);
      const e2 = Math.abs(s.afterHookX - boatAtLanding - target);
      if (e1 <= e2 && e1 < 0.12) await k.press('Space');
    }
    await page.waitForTimeout(6);
  }
  // Hold on the departure and the end line.
  while (Date.now() < end) await page.waitForTimeout(50);
}
