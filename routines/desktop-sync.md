# Desktop-linked session — submit approved moves + sync logs (run manually: "sync fantasy")

Not scheduled. Colby opens this task in the desktop app (or says "sync fantasy" in any desktop-linked session) whenever his computer is
open. Requires Claude in Chrome connected and the `fantasy-football` folder connected.

## Steps
1. Read Drive `approval-*.json` (latest file per decision_id wins). For each with `status: approved` and a deadline still ≥ 1 hour away: open ESPN in Chrome,
   make the move, confirm it took (read the roster back), create a new `approval-<decision_id>.json` with `status: submitted` and update the repo decision line
   `human_action.submitted_by: claude`. If the deadline passed, write `status: expired` and log the miss as `tooling_limit`.
   Ask Colby before each submit if he is present (per-action approval still stands if anything about the move changed since approval).
2. Log sync is automatic: `bridge/publish.ps1` runs `bridge/sync_logs.py` twice daily (5:30 / 18:30), merging every Drive inbox file
   (`decisions-*.jsonl`, `sessions-*.jsonl`, `replies-*.jsonl`, `scores-*.jsonl`, `weekly-W##.md`, `playbook-add-*.md`) into `logs/` and
   `playbook.md` by id, then pushing. Here, only check `bridge/publish.log` for a `sync: FAILED validation` line; if present, run
   `python bridge/sync_logs.py` by hand, read the errors, and fix the offending inbox line. The bridge never modifies the inbox.
3. Commit anything you changed here: `git add -A && git commit -m "sync: through W##" && git push`.
4. Report: what was submitted, what expired, the last `sync:` line from `bridge/publish.log`, validator result.
