# Context Package — what to give a Claude that manages your fantasy team

This is the article's transferable deliverable. It is the exact context, in priority order, that made Claude effective in this league,
plus the techniques that mattered and the ones that didn't. Copy the "Paste-in" block, fill the brackets, and hand it to your Claude.
It will be updated through the season as `playbook.md` confirms or refutes each item.

## Tier 1 — without this, every recommendation is generic
1. **Your league's scoring, verbatim.** Not "PPR" — the table. Ours has 0.5/rec, and D/ST scores *only* return TDs and safeties, which makes every public D/ST ranking wrong for us.
2. **Roster slots and limits.** 2 FLEX changes RB/WR scarcity math (7 starters × teams). Position caps (RB 6, WR 6, TE 2, QB 2) shape late rounds.
3. **League size, draft position, and keepers.** Keepers remove players *and* consume rounds — ours took AJB out of R2. Keeper round costs tell Claude which picks are dead.
4. **Your evaluation lens, stated.** Ours: age, injury history, opportunity/spotlight (vacated targets, roster holes), bye stacking cap (2 starters), tier gap before projection, and "give me a gut call." Without this, Claude ranks by projection.
5. **Deadlines and your availability.** Waiver clear time, lineup locks, when you can approve. Ours: never last minute, push to phone, 12-hour rule.

## Tier 2 — turns a good pick into a managed season
6. **Autonomy rule.** Propose → approve → submit. Say explicitly whether Claude may ever act without you (ours: never).
7. **The baselines you'll grade against.** Hindsight-optimal, the platform's autopick/projection, league W/L. Claude designs its logging around what you'll measure.
8. **Your risk posture.** Are you drafting for ceiling or floor? Will you carry a lottery ticket (we did: Brooks)? How many bench slots go to handcuffs?
9. **The platform's quirks.** ESPN's player table is virtualized (Claude sees ~15 rows at a time); Q tags need a hover; the draftable pool ≠ NFL depth charts (Justice Hill wasn't in it).
10. **What you'll override on.** Tell Claude where you'll trust your gut (we did on McBride > Bowers) so it can plan around it instead of arguing.

## Tier 3 — makes the log useful later
11. Session metadata: model in use, surface (live app / scheduled / Chrome), tools available, clock pressure.
12. Standing answers file so nothing gets re-asked.
13. A weekly "what did we learn" slot that writes to a playbook.

## Techniques that mattered (draft night evidence)
| Technique | Effect | Evidence |
|---|---|---|
| Pre-computed tier table + premortem before the clock | Enabled 12-second answers; predicted the QB run and RB cliff | W00-001, W00-005, W00-006 |
| "Three ranked choices" format | Survived picks being sniped; user always had a next name | W00-008, W00-010 |
| Queue 3 names in the platform before each pick | Prevents autopick disasters (Dak in a 1-QB league) | W00-011 |
| Background subagent for sleeper/handcuff research mid-draft | Produced sourced list without blocking pick advice | S-20260907-01 |
| Asking the user to hover Q tags | Only way to read injury notes live | S-20260907-01 |
| Pushback prompts ("be realistic", "gut feeling") | Forced league-specific reasoning over generic ranks | W00-003, W00-015 |

## Techniques that did not matter (so far)
- Model tier. Fable vs Sonnet would not have changed a draft pick; latency and pre-work did. To be re-tested on in-season research quality.
- Full-board reads. Impossible live; position filters are the unit of work.

## Paste-in block
```
You are managing my fantasy football team. League: [platform], [N] teams, scoring: [paste table]. Roster: [slots], limits: [caps].
My draft slot: [n]. Keepers (mine and others, with round cost): [list]. Deadlines: waivers clear [day/time], lineups lock [rule].
I can approve between [windows]; never propose anything last-minute; push to my phone. You never submit without my explicit yes.
Evaluate players on: age, injury history, opportunity (vacated targets/carries, depth-chart holes), bye stacking (max [2] starters/bye),
tier gap before projection. Always give a gut call and name the alternative. Grade yourself against: hindsight-optimal, the platform's
projection/autopick, and my W/L. Log every recommendation with reasoning, sources, confidence, what I actually did, and the outcome.
Platform quirks: [e.g. virtualized tables, Q tags need hover]. I will override on: [where you trust your gut].
```
