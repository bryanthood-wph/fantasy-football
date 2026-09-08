# Sunday 8 AM ET — Lineup (v1)

[COMMON preamble applies]

## Steps
1. Kickoffs: 1 PM ET lock is 5 hours away — the 12-hour rule applies to EVERY Sunday move. Every change is made by Colby in the ESPN app.
   Say this in the first line of the push.
2. Final injury check (Saturday/Sunday-morning reports, inactives are ~90 min pre-kickoff so flag anyone still uncertain and give the
   pivot: "if X is inactive, start Y").
3. Build the optimal lineup for QB, RB×2, WR×2, TE, FLEX×2, K, D/ST. For each contested slot (usually FLEX and WR2), give: the pick,
   the alternative, the projection for both (ESPN as baseline), and the lens reason that decides it (matchup, role, weather, Vegas
   total/implied points, injury to teammates that changes targets). Weather for outdoor games: search it.
4. Compare to the lineup currently set in league state. List ONLY the changes as `SLOT: OUT -> IN`. If no changes, say so.
5. Log one decision line per contested slot (not per player), with `baselines.espn_projection_choice` = the higher-projected player.
   Session line.
6. Push per COMMON: changes first, then "no-change confirmations" in one line, then the inactive pivots.
