import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from schema.validate import validate_decision, validate_file, validate_session  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def _good_decision() -> dict:
    return {
        "id": "2026-W01-001",
        "ts": "2026-09-13T12:00:00-04:00",
        "week": 1,
        "phase": "lineup",
        "claude_rec": {
            "choice": "TreVeyon Henderson",
            "alternatives": ["Tony Pollard"],
            "confidence": 0.6,
            "reasoning": "higher projection, lead back",
            "lens": {"age": "24", "injury": "Q", "opportunity": "Stevenson gone", "bye": "11", "tier_gap": "+6"},
            "sources": ["ESPN 2026 proj"],
        },
        "baselines": {"espn_projection_choice": "TreVeyon Henderson", "espn_autopick": None, "espn_rank_of_rec": 97},
        "human_action": {"choice": "TreVeyon Henderson", "followed": "yes", "override_reason": None, "submitted_by": "human"},
        "outcome": {},
        "technique": {"model": "claude-fable-5-1", "session_type": "scheduled", "prompt_pattern": "routine/sunday-lineup v1", "tools": ["WebSearch"], "time_to_decision_s": 40, "failures": []},
        "article": {"category": "pending", "anecdote": False, "note": ""},
    }


def test_good_decision_passes():
    assert validate_decision(_good_decision(), 1) == []


def test_bad_phase_fails():
    d = _good_decision()
    d["phase"] = "bench"
    assert any("phase" in e for e in validate_decision(d, 1))


def test_missing_lens_fails():
    d = _good_decision()
    del d["claude_rec"]["lens"]
    assert any("lens" in e for e in validate_decision(d, 1))


def test_session_requires_failures_list():
    s = {"id": "S-1", "ts_start": "x", "model": "m", "surface": "scheduled", "tools": [], "decisions": [], "failures": "none"}
    assert validate_session(s, 1)


def test_repo_logs_validate():
    for name in ("decisions.jsonl", "sessions.jsonl"):
        p = ROOT / "logs" / name
        if p.exists():
            assert validate_file(p) == [], validate_file(p)


def test_no_duplicate_ids_in_repo_log():
    p = ROOT / "logs" / "decisions.jsonl"
    if p.exists():
        ids = [json.loads(l)["id"] for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        assert len(ids) == len(set(ids))
