# Monday 9 PM ET — Outcomes, scoring, playbook (v1)

[COMMON preamble applies]

## Steps
1. Result: from league state scoreboard (MNF may still be in progress — say so and note that final scoring happens Tuesday's run if
   needed). Record W/L, points for/against, standing, and our lineup's actual points vs the optimal lineup from our roster (bench points
   left on the bench).
2. Score last week's decisions (every merged decision without a score, weeks ≤ current): write `scores-<run_id>.jsonl`, one line per
   decision — {decision_id, scored_at, pts_rec, pts_action, pts_optimal (best available at that moment), pts_espn_choice,
   hindsight_optimal, category}. Set category (claude_win / claude_miss / human_win / human_error / tooling_limit / tie) using the material-margin rules.
   For draft picks (week 0), update season-to-date points each Monday; they stay `pending` until Week 8, then get a provisional category.
3. Tally to date: counts by category; Claude-rec points vs human-action points vs ESPN-baseline points; override rate; how many decisions
   were shaped by tooling limits. Keep it honest — a bad week for Claude is data.
4. Playbook: create `playbook-add-<run_id>.md` in Drive with one to three lessons (evidence ids, status hypothesis/confirmed/refuted) and
   any open-hypothesis status changes. Desktop sync merges it into the repo `playbook.md`.
5. Weekly summary: create `weekly-W##.md` in the Drive folder — result, the decisions table (rec / action / optimal / category), the
   lessons, and an "anecdote candidates" list (any decision with `anecdote: true` or a Colby reply worth quoting).
6. Context-package check: did anything this week reveal context a reader's Claude would need (a scoring quirk, a platform behavior, a
   preference of Colby's)? Draft the line to add to `context-package.md` and include it in the push for approval.
7. Session line. If today is the first Monday of November, remind Colby that the routine cron times are in UTC and shift by one hour at
   the DST change (he can ask Claude to update them).
8. Push per COMMON: result line, tally line, the top lesson, and the optional human-notes question.
