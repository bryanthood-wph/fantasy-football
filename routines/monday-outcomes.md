# Monday 9 PM ET — Outcomes, scoring, playbook (v1)

[COMMON preamble applies]

## Steps
1. Result: from league state scoreboard (MNF may still be in progress — say so and note that final scoring happens Tuesday's run if
   needed). Record W/L, points for/against, standing, and our lineup's actual points vs the optimal lineup from our roster (bench points
   left on the bench).
2. Score last week's decisions (every line with `outcome == {}` from weeks ≤ current): fill `outcome` per the schema — `pts_rec`,
   `pts_action`, `pts_optimal` (best available at that moment), `pts_espn_choice`, `hindsight_optimal`, `scored_at`. Set
   `article.category` (claude_win / claude_miss / human_win / human_error / tooling_limit / tie) using the material-margin rules.
   For draft picks (week 0), update season-to-date points each Monday; they stay `pending` until Week 8, then get a provisional category.
3. Tally to date: counts by category; Claude-rec points vs human-action points vs ESPN-baseline points; override rate; how many decisions
   were shaped by tooling limits. Keep it honest — a bad week for Claude is data.
4. Playbook: append to the Drive copy of `playbook.md` (and note in the push that the repo copy syncs next desktop session): one to three
   lessons with evidence ids and status (hypothesis/confirmed/refuted). Re-check the open hypotheses; move any with enough evidence.
5. Weekly summary: write `weekly/W##.md` in the Drive folder — result, the decisions table (rec / action / optimal / category), the
   lessons, and an "anecdote candidates" list (any decision with `anecdote: true` or a Colby reply worth quoting).
6. Context-package check: did anything this week reveal context a reader's Claude would need (a scoring quirk, a platform behavior, a
   preference of Colby's)? Draft the line to add to `context-package.md` and include it in the push for approval.
7. Session line. If today is the first Monday of November, remind Colby that the routine cron times are in UTC and shift by one hour at
   the DST change (he can ask Claude to update them).
8. Push per COMMON: result line, tally line, the top lesson, and the optional human-notes question.
