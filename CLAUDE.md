# x-gaming

The owner collects ideas here for building games, specifically blockchain games: X posts, GitHub repos and other links that could help.

## When the owner shares a link

- Check `sources/` first: a link can come back (Sumiro was shared on 2026-11-04 and again on 2026-11-07), and a repeat gets a dated recheck section in its existing note, not a second note.
- Open X links with Claude in Chrome (the owner's Chrome profile), as the owner asked on 2026-11-04.
  Read the whole thread, the author's own replies and every linked repo or demo.
  On 2026-11-07 that profile was signed out of X: the author's thread still read in full, but other people's replies were cut off behind a sign-in wall.
  Later that day it was signed in again, so check before assuming either.
  For an X Article, Chrome's page-text tools cut each paragraph short and return at most about 1,000 characters per script call; the free `https://api.fxtwitter.com/<user>/status/<id>` returns the whole article as JSON, with code blocks in `article.content.entityMap` (Kensei, 2026-11-07).
- Check claims instead of repeating them: play the demo, inspect the repo, and measure what can be measured (load size, fps, cost).
- Write one note per source at `sources/YYYY-MM-DD-<author>-<slug>.md`, where the date is the day the source was added, with the same sections as the existing notes: verdict, what the source says, what it leaves out, what was checked, what helps us, blockchain fit, next step.
- When a source improves how we build, merge the change into `WORKFLOW.md` and cite the note.
- Add one entry at the top of the Sources list in `README.md` (date, linked title, author, one-line description, verdict), and any new reusable tool to its list.
- Save every note to the public repo, github.com/imDev2023/x-gaming, by committing and pushing to `main`, as the owner asked on 2026-11-04.
- Because the repo is public, paraphrase posts and link to them instead of copying their text, and never commit screenshots of other people's work, keys or anything private.
- Generation calls (fal, OpenAI and the like) are paid and need the owner's approval each time.
  Afterwards read fal's exact charge with `FAL_BILLING_KEY` (see WORKFLOW.md's Costs) and log that, not the estimate, in the spend ledger.

## Traps found so far

- Read `WORKFLOW.md` before any asset work: it holds the pipeline, the bridge's launch command, the safe-mode script rules and the done checks.
  Templates: [one prop](calibration/2026-11-06-crate-bridge/README.md), [a set of props](calibration/2026-11-06-kit/README.md) and [a whole game](calibration/2026-11-06-video2game/README.md); the Three.js check page is `calibration/2026-11-05-crate/viewer.html?src=<glb>`, with `src` repeated for a lineup.
- Dockstack's code now lives in `../dockstack` (github.com/imDev2023/dockstack), which deploys dockstack.vercel.app; make game changes there and follow its CLAUDE.md.
  `calibration/2026-11-06-video2game/game/` is the frozen calibration record: never run its `deploy.sh --prod`, since that would put the older game over the live one.
- Lantern River, the game for #6, lives in `../lantern-river` (github.com/imDev2023/lantern-river); make its changes there and follow its CLAUDE.md, which holds its rules, stage and Solana plans.
- Each calibration's `raw/` folder is gitignored and holds the only copy of its paid fal outputs and full-length takes; never delete it.
- The Video2Game skill is not installed: calibration 4 ran it from a clone of `lovisdotio/video-to-game` at `d1a24fd`, so reinstall or reclone it before another game run.
- MCP for Blender is installed at local scope with safe mode on and telemetry off (remove with `claude mcp remove blender -s local`).
  Auto mode refuses to install MCP servers or Blender add-ons, so the owner runs those with `!`, and new tools load only in a later session.
- `reference/aioriented/` (the owner's VibeGameDev member repos) and `.claude/skills/` (15 skills copied from vgd-skills v3.6.0) are gitignored and local only: never commit or push them, and paraphrase rather than copy from them, as with any source.
  To update the skills, pull `reference/aioriented/vgd-skills` and copy the same folders again.
- For a gameplay video, use `../dockstack/tools/render-video.mjs` (see its README section): Chrome's live screencast dropped and reordered frames, so it renders frame by frame on a virtual clock and mixes the sound in Node, because headless Chrome refused to allocate a 60 s buffer for offline mixing.
- Start Blender's GUI for the bridge with `run_in_background` and stop it with TaskStop; it leaves the owner's Blender preferences unchanged.

## Multica dashboard

This project is mirrored on the owner's Multica dashboard (workspace Pandora) as project `5e65d424-8653-4e40-8aca-449c8e90891c`.
GitHub Issues on `imDev2023/x-gaming` stay the source of truth; Multica only mirrors them, and each Multica ticket title starts with its issue number (for example `#1`).
At the end of every session, after the issues are updated, run the `multica-sync` skill for this project: mirror ticket statuses, add any new tickets, and refresh the project's "Current step" section.
Every status and assignment write passes `--no-start` (`issue create` rejects the flag and starts nothing while the assignee is a member), and no ticket is ever assigned to an agent, so the sync never starts an agent run.
If the `multica` CLI is not signed in, say so in the session summary and stop anyway; the sync never blocks the work.
