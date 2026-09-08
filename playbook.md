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
