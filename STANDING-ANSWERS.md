# Standing Answers — fantasy-football

Confirmed by Colby. Routines and sessions apply these without re-asking. One dated line each.

- 2026-09-07 — Autonomy: propose → Colby approves → submit. Every ESPN transaction needs his explicit per-action yes. Never auto-submit.
- 2026-09-07 — Independence: routines run cloud-side and push to his phone. They must never depend on his computer being open.
- 2026-09-07 — 12-hour rule: if the deadline is under 12 hours away, the push tells him to submit in the ESPN app himself and the log records `submitted_by: human`. Otherwise approved moves queue for the next desktop-linked session (`submitted_by: claude`).
- 2026-09-07 — Not last minute: waiver proposals Tue 7 PM ET (clear Wed ~3 AM); lineup proposals Sun 8 AM ET; Thu 7 PM ET injury/TNF check; Mon 9 PM ET outcome log.
- 2026-09-07 — Trades: weekly scan + proposals only. Colby sends offers himself.
- 2026-09-07 — Grading baselines: hindsight-optimal, ESPN projection/autopick, league W/L. Also log Claude rec vs. human action.
- 2026-09-07 — Logging: `.jsonl` canonical, Markdown weekly summaries, git-tracked. Log a lot.
- 2026-09-07 — Evaluation lens: age, injury history, opportunity/spotlight, bye stacking, tier gaps — never rankings or ESPN projections alone. Always include a gut call.
- 2026-09-07 — Article intent: Claude's effectiveness vs. where a human was necessary; the experience itself; a framework readers can hand their own Claude (context package, models, techniques). Learn and evolve weekly; anecdotes matter.
- 2026-09-07 — Credentials: Claude never handles ESPN cookies. The bridge script runs locally with a `.env` that stays on Colby's machine.
- 2026-09-07 — Live data bridge: local `espn_api` script → `state/league-state.json` → public GitHub repo. Cloud routines read the raw URL from `config.json` in the Drive log folder.
