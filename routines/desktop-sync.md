# Desktop-linked session — submit approved moves + sync logs (run manually: "sync fantasy")

Not scheduled. Colby opens this task in the desktop app (or says "sync fantasy" in any desktop-linked session) whenever his computer is
open. Requires Claude in Chrome connected and the `fantasy-football` folder connected.

## Steps
1. Read Drive `pending-approvals.json`. For each item with `status: approved` and a deadline still ≥ 1 hour away: open ESPN in Chrome,
   make the move, confirm it took (read the roster back), set `status: submitted`, and update the decision line
   `human_action.submitted_by: claude`. If the deadline passed, set `status: expired` and log the miss as `tooling_limit`.
   Ask Colby before each submit if he is present (per-action approval still stands if anything about the move changed since approval).
2. Sync logs: append Drive `decisions.jsonl` and `sessions.jsonl` lines not yet in the repo's `logs/` files (by id); copy Drive
   `weekly/W##.md` and the Drive `playbook.md` additions into the repo. Run `python schema/validate.py` and `pytest`; fix before committing.
3. `git add -A && git commit -m "sync: through W##" && git push` (the state file is already pushed nightly by the bridge).
4. Report: what was submitted, what expired, how many lines synced, validator result.
