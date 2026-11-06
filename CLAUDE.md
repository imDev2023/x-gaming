# x-gaming

The owner collects ideas here for building games, specifically blockchain games: X posts, GitHub repos and other links that could help.

## When the owner shares a link

- Open X links with Claude in Chrome (the owner's logged-in Chrome profile), as the owner asked on 2026-11-04.
  Read the whole thread, the author's own replies and every linked repo or demo.
- Check claims instead of repeating them: play the demo, inspect the repo, and measure what can be measured (load size, fps, cost).
- Write one note per source at `sources/YYYY-MM-DD-<author>-<slug>.md`, where the date is the day the source was added, with the same sections as the existing notes: verdict, what the source says, what it leaves out, what was checked, what helps us, blockchain fit, next step.
- When a source improves how we build, merge the change into `WORKFLOW.md` and cite the note.
- Add one entry at the top of the Sources list in `README.md` (date, linked title, author, one-line description, verdict), and any new reusable tool to its list.
- Save every note to the public repo, github.com/imDev2023/x-gaming, by committing and pushing to `main`, as the owner asked on 2026-11-04.
- Because the repo is public, paraphrase posts and link to them instead of copying their text, and never commit screenshots of other people's work, keys or anything private.
- Generation calls (fal, OpenAI and the like) are paid and need the owner's approval each time.

## Traps found so far

- Our pipeline and its done checks live in `WORKFLOW.md`; hands-on tests live in `calibration/` (start with [calibration/2026-11-05-crate](calibration/2026-11-05-crate/README.md)).
- MCP for Blender is installed (local scope, `BLENDER_MCP_SAFE_MODE=1`, `DISABLE_TELEMETRY=true`; remove with `claude mcp remove blender -s local`).
  Auto mode refuses to install MCP servers or Blender add-ons, so the owner runs those with `!`; the tools load only in a session started afterwards.
- The add-on's server never starts under `blender -b`, so the bridge needs the Blender GUI.
  Launch `/Applications/Blender.app/Contents/MacOS/Blender --addons blender_mcp` with `run_in_background` to enable it for that run without changing the owner's Blender preferences (not yet tried); it listens on localhost:9876.
- Blender's look renders show shape, not final color: judge color and metal in Three.js with an environment map.

## Multica dashboard

This project is mirrored on the owner's Multica dashboard (workspace Pandora) as project `5e65d424-8653-4e40-8aca-449c8e90891c`.
GitHub Issues on `imDev2023/x-gaming` stay the source of truth; Multica only mirrors them, and each Multica ticket title starts with its issue number (for example `#1`).
At the end of every session, after the issues are updated, run the `multica-sync` skill for this project: mirror ticket statuses, add any new tickets, and refresh the project's "Current step" section.
Every Multica write passes `--no-start` and no ticket is ever assigned to an agent, so the sync never starts an agent run.
If the `multica` CLI is not signed in, say so in the session summary and stop anyway; the sync never blocks the work.
