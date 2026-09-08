"""Validate fantasy-football .jsonl logs against schema/DECISION-LOG.md.

Usage:
    python schema/validate.py logs/decisions.jsonl [logs/sessions.jsonl ...]

Exit code 0 = all lines valid. Prints one error per bad line.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PHASES = {"draft", "waiver", "lineup", "trade", "stream"}
FOLLOWED = {"yes", "partial", "no"}
SUBMITTED_BY = {"claude", "human", "autopick"}
CATEGORIES = {
    "claude_win",
    "claude_miss",
    "human_win",
    "human_error",
    "tooling_limit",
    "tie",
    "pending",
}
SESSION_TYPES = {"live", "scheduled", "desktop-linked"}

DECISION_REQUIRED = {
    "id",
    "ts",
    "week",
    "phase",
    "claude_rec",
    "baselines",
    "human_action",
    "technique",
    "article",
}
SESSION_REQUIRED = {"id", "ts_start", "model", "surface", "tools", "decisions", "failures"}


def _err(line_no: int, msg: str) -> str:
    return f"line {line_no}: {msg}"


def validate_decision(obj: dict, line_no: int) -> list[str]:
    errors: list[str] = []
    missing = DECISION_REQUIRED - obj.keys()
    if missing:
        errors.append(_err(line_no, f"missing {sorted(missing)}"))
        return errors
    if obj["phase"] not in PHASES:
        errors.append(_err(line_no, f"bad phase {obj['phase']!r}"))
    if not isinstance(obj["week"], int) or obj["week"] < 0:
        errors.append(_err(line_no, "week must be int >= 0"))
    rec = obj["claude_rec"]
    for key in ("choice", "reasoning", "lens", "sources", "confidence"):
        if key not in rec:
            errors.append(_err(line_no, f"claude_rec missing {key}"))
    if "confidence" in rec and not (0.0 <= float(rec["confidence"]) <= 1.0):
        errors.append(_err(line_no, "confidence must be 0..1"))
    ha = obj["human_action"]
    if ha.get("followed") not in FOLLOWED:
        errors.append(_err(line_no, f"human_action.followed must be one of {sorted(FOLLOWED)}"))
    if ha.get("submitted_by") not in SUBMITTED_BY:
        errors.append(_err(line_no, f"human_action.submitted_by must be one of {sorted(SUBMITTED_BY)}"))
    tech = obj["technique"]
    for key in ("model", "session_type", "prompt_pattern", "tools"):
        if key not in tech:
            errors.append(_err(line_no, f"technique missing {key}"))
    if tech.get("session_type") not in SESSION_TYPES:
        errors.append(_err(line_no, f"technique.session_type must be one of {sorted(SESSION_TYPES)}"))
    if obj["article"].get("category") not in CATEGORIES:
        errors.append(_err(line_no, f"article.category must be one of {sorted(CATEGORIES)}"))
    return errors


def validate_session(obj: dict, line_no: int) -> list[str]:
    missing = SESSION_REQUIRED - obj.keys()
    if missing:
        return [_err(line_no, f"missing {sorted(missing)}")]
    errors: list[str] = []
    if not isinstance(obj["tools"], list) or not isinstance(obj["decisions"], list):
        errors.append(_err(line_no, "tools and decisions must be lists"))
    if not isinstance(obj["failures"], list):
        errors.append(_err(line_no, "failures must be a list"))
    return errors


def validate_file(path: Path) -> list[str]:
    kind = "session" if "sessions" in path.name else "decision"
    fn = validate_session if kind == "session" else validate_decision
    errors: list[str] = []
    seen_ids: set[str] = set()
    with path.open(encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(_err(line_no, f"invalid JSON: {exc}"))
                continue
            errors.extend(fn(obj, line_no))
            if obj.get("id") in seen_ids:
                errors.append(_err(line_no, f"duplicate id {obj['id']}"))
            seen_ids.add(obj.get("id"))
    return errors


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    rc = 0
    for arg in argv:
        errs = validate_file(Path(arg))
        if errs:
            rc = 1
            print(f"{arg}: {len(errs)} error(s)")
            for e in errs:
                print("  " + e)
        else:
            print(f"{arg}: OK")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
