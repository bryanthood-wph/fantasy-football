# Playbook — evolving lessons

Updated every Monday by the outcome routine. Each entry: date, lesson, evidence (decision ids), status (`hypothesis` → `confirmed` / `refuted`).
This file is the raw material for the article's "framework" section. Keep it honest; refuted entries stay.

## Draft night (2026-09-07)

- **Pre-compute, then apply.** Tier tables and a premortem written before the clock started made 12-second picks possible. Under the clock, Claude is a lookup + judgment engine, not a researcher. — evidence: W00-001, W00-006 — `confirmed`
- **The room drafts QBs early.** Premortem #4 predicted it; Allen R2, Lamar R5, three T2 QBs gone by R7. Take a T2 QB at the first even-round pick after R5 in this league. — W00-005 — `confirmed`
- **RB T2 vanishes between picks 5 and 25.** Predicted at 55%, happened. TE pivot at 25 is the right plan B in a 2-FLEX league. — W00-002 — `confirmed`
- **User overrides cluster under time pressure and on "feel" picks.** Brooks (W00-007) and Jamo-over-QB (W00-005) were both instant decisions with the rec on screen. Hypothesis: a queued top-3 reduces overrides. — `hypothesis`
- **The lens beat the number three times and lost zero.** Odunze over projection-higher WRs, Dart over Burrow, Henderson over Brooks. Season points will settle it. — W00-004, W00-006, W00-008 — `hypothesis`
- **Check the platform's player pool before planning handcuffs.** Justice Hill was not draftable on ESPN; sleeper research was built from NFL depth charts, not the ESPN universe. — W00-013 — `confirmed`
- **Tool latency is the binding constraint, not model quality.** One page read = 15–40s on a 60–90s clock. Fable vs Sonnet would not have changed a pick; the pre-work did. — S-20260907-01 — `confirmed`
- **The board is a window, not a list.** ESPN virtualizes the player table; text extraction returns 10–20 rows. Position filters + scrolling are mandatory; full-board reads are impossible live. — S-20260907-01 — `confirmed`
- **Users challenge good recs when they sound generic.** "Be realistic — Eagles won't be there" produced a better framing (returner lens for a return-TD-only D/ST scoring) that was right but late. Lead with the league-specific angle. — W00-015 — `confirmed`
- **Autopick would have made two bad picks.** ARSB at 5 (fine) but Dak at 116 in a 1-QB league and MHJ at 76. Baseline for "did Claude beat the default" is real. — W00-007, W00-011 — `confirmed`

## Open hypotheses to test in-season
- Does a queued top-3 before every pick/deadline reduce user overrides to <10%?
- Does the age/injury/opportunity lens outperform ESPN projection on waiver adds over a 4-week window?
- Is a Thursday injury check worth its cost (how many lineup changes does it produce)?
- What share of decisions end up `tooling_limit` vs `claude_miss`?

<!-- synced playbook-add-20260908-tue.md -->
# Playbook additions — run 20260908-tue (written 2026-09-09 00:40 UTC, session S-20260908-03)

Desktop sync: merge L-004 into playbook.md, add the standing answer to STANDING-ANSWERS.md, and paste the BRIEF RULE block into routines/COMMON.md so the repo copy matches the four scheduled-task prompts (all four were updated 2026-09-09 00:35–00:38 UTC).

## L-004 — Reasoning that lives only in the log never reaches the decision-maker
- status: confirmed (observed)
- added: 2026-09-09, S-20260908-03
- lesson: The v1.2 run wrote 48 KB of reasoning (three candidates, lens, priced projections, pre-flight, anticipated questions) into decisions-20260908-tue-2.jsonl and a 120-word push with only the picks. Colby, on his phone, saw picks without a why, overrode the waiver selection (Hill instead of Allgeier) and declined the trade — and said: "your analysis doesn't provide details on why you chose what you chose. this is a glaring opporutnity." The log is for scoring; the brief is for deciding. Every run now writes weekly/brief-<run_id>.md (pick, Why, Why not each losing candidate, Why drop X, What makes it wrong; prose, under 900 words) before the push, and the push carries one "because" clause per move plus `Why: weekly/brief-<run_id>.md`.
- generalizes to: any unattended routine whose output is consumed on a phone — the artifact that reaches the human must carry the argument, not a pointer to it.
- evidence: replies-20260908-tue-1.jsonl, replies-20260908-tue-2.jsonl, weekly/brief-20260908-tue.md (Drive id 1QGUNpSMkn20pShFpmqDtONNZ09282mPA)
- test: override rate on decisions whose brief was pushed vs the three from this run (2 of 3 overridden/declined with no brief). Re-check Week 6 alongside L-003 and the v1.2 safe-share test.

## Standing answer to add
- 2026-09-09 — Briefs: every recommendation run writes weekly/brief-<run_id>.md with the why for each pick and why each losing candidate lost, before pushing; the push carries one "because" clause per move. Colby: "make sure we get output like this everytime and log it".

## BRIEF RULE block (verbatim, as inserted into the four scheduled-task prompts after the PREAMBLE)
BRIEF RULE (v1.3, added 2026-09-09 — Colby, after run 20260908-tue: "your analysis doesn't provide details on why you chose what you chose. this is a glaring opportunity" / "make sure we get output like this everytime and log it"): The reasoning must reach the phone, not just the log. Every run that produces a recommendation or a score writes `brief-<run_id>.md` into the Drive `weekly` folder (folder id 1sTPoWolxmLCFQoED8dqAWeg0EDYKYtAX) BEFORE the push, modeled on `weekly/brief-20260908-tue.md`. One section per decision id: the pick; **Why** — 3-5 sentences of the specific facts that decided it (the ESPN number stated and priced, contested/uncontested, the deadline); **Why not <each losing candidate>** — named, one short paragraph each, on the merits not by implication; **Why drop/bench X** if a drop or bench is involved; **What makes it wrong** — the single condition. Prose, phone-readable, under 900 words, no tables. The push carries one "because" clause per move (the single decisive fact, e.g. `ADD Allgeier / DROP Jones — because he is the only FA RB with a starting job and the only one rivals will claim`) and ends with the line `Why: weekly/brief-<run_id>.md`. Record the brief's Drive file id as `brief_ref` in the session line. Reasoning that exists only inside decisions-*.jsonl does not count as delivered. Monday runs write the brief on the scoring: why each decision received its category and margin.

## Push-section edits made to each prompt
- Tue: moves are tagged with candidate type AND a 'because' clause.
- Thu / Sun: "the one reason that matters (a 'because' clause)" and a closing `Why: weekly/brief-<run_id>.md` line.
- Mon: closing `Why: weekly/brief-<run_id>.md` line.
