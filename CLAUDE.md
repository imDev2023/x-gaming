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

- `WORKFLOW.md` holds the pipeline, the Blender bridge's launch command, the safe-mode rules for bridge scripts and the done checks; read it before any asset work.
  Hands-on tests live in `calibration/`: [the crate by script](calibration/2026-11-05-crate/README.md), then [the crate through the bridge](calibration/2026-11-06-crate-bridge/README.md), whose `build.py`, `checks.py` and `export.py` are the templates for new props.
- MCP for Blender is installed (local scope, `BLENDER_MCP_SAFE_MODE=1`, `DISABLE_TELEMETRY=true`; remove with `claude mcp remove blender -s local`).
  Auto mode refuses to install MCP servers or Blender add-ons, so the owner runs those with `!`; the tools load only in a session started afterwards.
- The bridge needs Blender's GUI, since its server never starts under `blender -b`: start it with `run_in_background`, which leaves the owner's Blender preferences unchanged, and stop it with TaskStop when done.
- Workbench renders with cavity and outlines draw edges and colors the engine never shows, so judge face-on detail, color and metal in Material Preview or the Three.js check page, `calibration/2026-11-05-crate/viewer.html?src=<glb>`.

## Multica dashboard

This project is mirrored on the owner's Multica dashboard (workspace Pandora) as project `5e65d424-8653-4e40-8aca-449c8e90891c`.
GitHub Issues on `imDev2023/x-gaming` stay the source of truth; Multica only mirrors them, and each Multica ticket title starts with its issue number (for example `#1`).
At the end of every session, after the issues are updated, run the `multica-sync` skill for this project: mirror ticket statuses, add any new tickets, and refresh the project's "Current step" section.
Every Multica write passes `--no-start` and no ticket is ever assigned to an agent, so the sync never starts an agent run.
If the `multica` CLI is not signed in, say so in the session summary and stop anyway; the sync never blocks the work.
