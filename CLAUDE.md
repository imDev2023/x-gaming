# x-gaming

The owner collects ideas here for building games, specifically blockchain games: X posts, GitHub repos and other links that could help.

## When the owner shares a link

- Open X links with Claude in Chrome (the owner's logged-in Chrome profile), as the owner asked on 2026-11-04.
  Read the whole thread, the author's own replies and every linked repo or demo.
- Check claims instead of repeating them: play the demo, inspect the repo, and measure what can be measured (load size, fps, cost).
- Write one note per source at `sources/YYYY-MM-DD-<author>-<slug>.md`, with the same sections as the existing notes: verdict, the process, what the post leaves out, what was checked, reusable pieces, feasibility for us, blockchain fit, next step.
- Add one row to the Sources table in `README.md`, and any new reusable tool to its list.
- Generation calls (fal, OpenAI and the like) are paid and need the owner's approval each time.

## Multica dashboard

This project is mirrored on the owner's Multica dashboard (workspace Pandora) as project `5e65d424-8653-4e40-8aca-449c8e90891c`.
There is no local tracker yet, so the Multica tickets themselves are the source of truth: update them directly instead of mirroring.
At the end of every session, run the `multica-sync` skill for this project: update ticket statuses, add any new tickets, and refresh the project's "Current step" section.
Every Multica write passes `--no-start` and no ticket is ever assigned to an agent, so the sync never starts an agent run.
If the `multica` CLI is not signed in, say so in the session summary and stop anyway; the sync never blocks the work.
