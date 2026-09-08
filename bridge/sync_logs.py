"""Drain the Drive inbox (cloud-run logs) into the repo. Never modifies the inbox.

Cloud routines can only create files on Drive, so they write one file per run
(see config.json log_convention). This merges those files into the repo logs by id,
validates the merged result, and writes nothing if validation fails.

Usage:
    python bridge/sync_logs.py                 # inbox = %FF_INBOX% or G:\\My Drive\\fantasy-football-logs
    python bridge/sync_logs.py --inbox DIR --root DIR

Exit 0 = merged (or nothing to do). Exit 1 = merged result failed validation; repo untouched.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from schema.validate import validate_decision, validate_session  # noqa: E402

DEFAULT_INBOX = os.environ.get("FF_INBOX", r"G:\My Drive\fantasy-football-logs")
REPLY_FIELDS = ("reply", "choice", "followed", "override_reason", "submitted_by")
SCORE_FIELDS = ("pts_rec", "pts_action", "pts_optimal", "pts_espn_choice", "hindsight_optimal", "scored_at")


def _lines(path: Path) -> list[dict]:
    out = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if raw:
            out.append(json.loads(raw))
    return out


def _load(path: Path) -> dict[str, dict]:
    return {o["id"]: o for o in _lines(path)} if path.exists() else {}


def _dump(objs) -> str:
    return "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs)


def sync(inbox: Path, root: Path) -> tuple[int, dict, list[str]]:
    decisions = _load(root / "logs" / "decisions.jsonl")
    sessions = _load(root / "logs" / "sessions.jsonl")
    stats = dict(decisions=0, sessions=0, replies=0, scores=0, weekly=0, playbook_adds=0)
    warnings: list[str] = []
    pending_writes: dict[Path, str] = {}

    # Convention names only (config.log_convention); legacy single-file logs on Drive are ignored.
    for f in sorted(inbox.glob("decisions-*.jsonl")):
        for o in _lines(f):
            if o.get("id") and o["id"] not in decisions:
                decisions[o["id"]] = o
                stats["decisions"] += 1

    for f in sorted(inbox.glob("sessions-*.jsonl")):
        for o in _lines(f):
            if o.get("id") and o["id"] not in sessions:
                sessions[o["id"]] = o
                stats["sessions"] += 1

    for f in sorted(inbox.glob("replies-*.jsonl")):
        for r in _lines(f):
            d = decisions.get(r.get("decision_id"))
            if not d:
                warnings.append(f"{f.name}: unknown decision_id {r.get('decision_id')!r}, skipped")
                continue
            ha = d.setdefault("human_action", {})
            for k in REPLY_FIELDS:
                if k in r:
                    ha[k] = r[k]
            if r.get("override_reason"):
                d.setdefault("article", {})["anecdote"] = True
            stats["replies"] += 1

    for f in sorted(inbox.glob("scores-*.jsonl")):
        for s in _lines(f):
            d = decisions.get(s.get("decision_id"))
            if not d:
                warnings.append(f"{f.name}: unknown decision_id {s.get('decision_id')!r}, skipped")
                continue
            out = d.setdefault("outcome", {})
            for k in SCORE_FIELDS:
                if k in s:
                    out[k] = s[k]
            if "category" in s:
                d.setdefault("article", {})["category"] = s["category"]
            stats["scores"] += 1

    errors: list[str] = []
    for n, o in enumerate(decisions.values(), start=1):
        errors += [f"decisions {o.get('id')}: {e}" for e in validate_decision(o, n)]
    for n, o in enumerate(sessions.values(), start=1):
        errors += [f"sessions {o.get('id')}: {e}" for e in validate_session(o, n)]
    if errors:
        return 1, stats, errors

    if any(stats[k] for k in ("decisions", "replies", "scores")):
        pending_writes[root / "logs" / "decisions.jsonl"] = _dump(decisions.values())
    if stats["sessions"]:
        pending_writes[root / "logs" / "sessions.jsonl"] = _dump(sessions.values())

    weekly_src = list(inbox.glob("weekly-W*.md")) + list((inbox / "weekly").glob("W*.md"))
    for f in sorted(weekly_src):
        name = f.name[len("weekly-"):] if f.name.startswith("weekly-") else f.name
        dest = root / "logs" / "weekly" / name
        content = f.read_text(encoding="utf-8")
        if not dest.exists() or dest.read_text(encoding="utf-8") != content:
            pending_writes[dest] = content
            stats["weekly"] += 1

    playbook = root / "playbook.md"
    pb_text = playbook.read_text(encoding="utf-8") if playbook.exists() else ""
    for f in sorted(inbox.glob("playbook-add-*.md")):
        marker = f"<!-- synced {f.name} -->"
        if marker not in pb_text:
            pb_text = pb_text.rstrip("\n") + f"\n\n{marker}\n{f.read_text(encoding='utf-8').strip()}\n"
            stats["playbook_adds"] += 1
    if stats["playbook_adds"]:
        pending_writes[playbook] = pb_text

    for path, text in pending_writes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return 0, stats, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inbox", default=DEFAULT_INBOX)
    ap.add_argument("--root", default=str(ROOT))
    args = ap.parse_args()
    inbox = Path(args.inbox)
    if not inbox.is_dir():
        print(f"sync: inbox not found: {inbox} (Drive not mounted?) - nothing to do")
        return 0
    rc, stats, notes = sync(inbox, Path(args.root))
    summary = ", ".join(f"{v} {k}" for k, v in stats.items())
    if rc:
        print(f"sync: FAILED validation, repo untouched ({summary})")
    else:
        print(f"sync: {summary}")
    for n in notes:
        print("  " + n)
    return rc


if __name__ == "__main__":
    sys.exit(main())
