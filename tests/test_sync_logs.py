import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bridge"))

from sync_logs import sync  # noqa: E402


def _decision(id_: str) -> dict:
    return {
        "id": id_,
        "ts": "2026-09-13T12:00:00-04:00",
        "week": 1,
        "phase": "lineup",
        "claude_rec": {
            "choice": "A",
            "alternatives": ["B"],
            "confidence": 0.6,
            "reasoning": "r",
            "lens": {"age": "", "injury": "", "opportunity": "", "bye": "", "tier_gap": ""},
            "sources": [],
        },
        "baselines": {"espn_projection_choice": "A", "espn_autopick": None, "espn_rank_of_rec": 1},
        "human_action": {"choice": None, "followed": "no", "override_reason": None, "submitted_by": "human"},
        "outcome": {},
        "technique": {"model": "m", "session_type": "scheduled", "prompt_pattern": "p", "tools": [], "time_to_decision_s": 1, "failures": []},
        "article": {"category": "pending", "anecdote": False, "note": ""},
    }


def _session(id_: str) -> dict:
    return {"id": id_, "ts_start": "x", "model": "m", "surface": "scheduled", "tools": [], "decisions": [], "failures": []}


def _jsonl(*objs) -> str:
    return "".join(json.dumps(o) + "\n" for o in objs)


def _make(tmp_path: Path):
    root, inbox = tmp_path / "repo", tmp_path / "inbox"
    (root / "logs").mkdir(parents=True)
    (inbox / "weekly").mkdir(parents=True)
    (root / "logs" / "decisions.jsonl").write_text(_jsonl(_decision("2026-W01-001")), encoding="utf-8")
    (root / "logs" / "sessions.jsonl").write_text(_jsonl(_session("S-20260907-01")), encoding="utf-8")
    (root / "playbook.md").write_text("# Playbook\n", encoding="utf-8")
    return root, inbox


def _ids(path: Path) -> list[str]:
    return [json.loads(l)["id"] for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def test_merges_new_lines_dedups_by_id_and_is_idempotent(tmp_path):
    root, inbox = _make(tmp_path)
    (inbox / "decisions-20260915-tue.jsonl").write_text(_jsonl(_decision("2026-W02-001"), _decision("2026-W01-001")), encoding="utf-8")
    (inbox / "sessions-20260915-tue.jsonl").write_text(_jsonl(_session("S-20260915-01")), encoding="utf-8")

    rc, stats, notes = sync(inbox, root)
    assert rc == 0 and notes == []
    assert stats["decisions"] == 1 and stats["sessions"] == 1
    assert _ids(root / "logs" / "decisions.jsonl") == ["2026-W01-001", "2026-W02-001"]
    assert _ids(root / "logs" / "sessions.jsonl") == ["S-20260907-01", "S-20260915-01"]

    rc, stats, _ = sync(inbox, root)
    assert rc == 0 and not any(stats.values())


def test_replies_and_scores_update_existing_decision(tmp_path):
    root, inbox = _make(tmp_path)
    (inbox / "replies-20260915-tue.jsonl").write_text(
        _jsonl({"decision_id": "2026-W01-001", "choice": "B", "followed": "no", "override_reason": "gut", "submitted_by": "human"}), encoding="utf-8"
    )
    (inbox / "scores-20260921-mon.jsonl").write_text(
        _jsonl({"decision_id": "2026-W01-001", "pts_rec": 10.0, "pts_action": 8.0, "category": "claude_win", "scored_at": "z"}), encoding="utf-8"
    )
    rc, stats, _ = sync(inbox, root)
    assert rc == 0 and stats["replies"] == 1 and stats["scores"] == 1
    d = json.loads((root / "logs" / "decisions.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert d["human_action"]["choice"] == "B" and d["article"]["anecdote"] is True
    assert d["outcome"]["pts_rec"] == 10.0 and d["article"]["category"] == "claude_win"


def test_unknown_decision_id_is_warned_not_fatal(tmp_path):
    root, inbox = _make(tmp_path)
    (inbox / "replies-x.jsonl").write_text(_jsonl({"decision_id": "nope", "followed": "yes"}), encoding="utf-8")
    rc, stats, notes = sync(inbox, root)
    assert rc == 0 and stats["replies"] == 0 and any("nope" in n for n in notes)


def test_invalid_inbox_line_blocks_all_writes(tmp_path):
    root, inbox = _make(tmp_path)
    bad = _decision("2026-W02-009")
    bad["phase"] = "bench"
    (inbox / "decisions-bad.jsonl").write_text(_jsonl(_decision("2026-W02-002"), bad), encoding="utf-8")
    (inbox / "weekly-W02.md").write_text("# W02\n", encoding="utf-8")
    before = (root / "logs" / "decisions.jsonl").read_text(encoding="utf-8")

    rc, _, errors = sync(inbox, root)
    assert rc == 1 and any("2026-W02-009" in e for e in errors)
    assert (root / "logs" / "decisions.jsonl").read_text(encoding="utf-8") == before
    assert not (root / "logs" / "weekly" / "W02.md").exists()


def test_weekly_and_playbook_adds(tmp_path):
    root, inbox = _make(tmp_path)
    (inbox / "weekly-W02.md").write_text("# W02\n", encoding="utf-8")
    (inbox / "weekly" / "W00.md").write_text("# W00\n", encoding="utf-8")
    (inbox / "playbook-add-20260921-mon.md").write_text("## L-004\nlesson\n", encoding="utf-8")

    rc, stats, _ = sync(inbox, root)
    assert rc == 0 and stats["weekly"] == 2 and stats["playbook_adds"] == 1
    assert (root / "logs" / "weekly" / "W02.md").read_text(encoding="utf-8") == "# W02\n"
    assert (root / "logs" / "weekly" / "W00.md").exists()
    pb = (root / "playbook.md").read_text(encoding="utf-8")
    assert pb.count("L-004") == 1 and "<!-- synced playbook-add-20260921-mon.md -->" in pb

    rc, stats, _ = sync(inbox, root)
    assert stats["weekly"] == 0 and stats["playbook_adds"] == 0
    assert (root / "playbook.md").read_text(encoding="utf-8").count("L-004") == 1


def test_inbox_never_modified(tmp_path):
    root, inbox = _make(tmp_path)
    f = inbox / "decisions-20260915-tue.jsonl"
    f.write_text(_jsonl(_decision("2026-W02-001")), encoding="utf-8")
    snapshot = {p.name: p.read_bytes() for p in inbox.rglob("*") if p.is_file()}
    sync(inbox, root)
    assert {p.name: p.read_bytes() for p in inbox.rglob("*") if p.is_file()} == snapshot
