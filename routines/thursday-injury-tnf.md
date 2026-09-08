# Thursday 7 PM ET — Injury check + Thursday-night starters (v1)

[COMMON preamble applies]

## Steps
1. Identify any of our players on Thursday Night Football (kickoff ~8:15 PM ET — the 12-hour rule always applies: any TNF change is
   in-app by Colby). If none, say so in one line.
2. Injury sweep: for every rostered player, search this week's practice reports and injury designations (Wed/Thu reports). Sources: team
   sites, ESPN/NFL injury pages, beat reporters. List anyone Q/D/O with the latest quote and a probability of playing (GUESS xx%).
3. Consequences: if a starter is likely out, name the replacement now from the bench and, if the bench cannot cover, the best
   free-agent pickup that could still be claimed/added before Sunday (free agency after waivers clear is first-come).
4. Waiver follow-up: did Tuesday's claims process? Read league state `recent_activity` and write a `replies-<run_id>-<n>.jsonl` line for each claim
   (processed / failed) so the decision's `human_action` can be resolved.
5. Log: one decision line per TNF lineup call or replacement recommendation; session line.
6. Push per COMMON: TNF moves (if any) + the injury watchlist for Sunday in ≤5 lines. If nothing to do: "No action".
