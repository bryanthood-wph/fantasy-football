"""Publish a credential-free snapshot of a private ESPN fantasy league.

Runs on YOUR machine. Reads ESPN with your session cookies from a local .env
(never committed), writes state/league-state.json (no secrets), which you then
git-push so cloud routines can read it from a public raw URL.

Usage:
    python bridge/espn_state.py                  # uses .env next to this file
    python bridge/espn_state.py --out path.json  # custom output

.env keys:
    ESPN_LEAGUE_ID=1594445542
    ESPN_SEASON=2026
    ESPN_TEAM_ID=5
    ESPN_S2=...      # from browser cookies (see SETUP.md)
    ESPN_SWID={...}  # from browser cookies, braces included
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
    from espn_api.football import League
except ImportError as exc:  # pragma: no cover
    sys.exit(f"missing dependency: {exc}. Run: pip install -r bridge/requirements.txt")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def _g(obj, name, default=None):
    """getattr that tolerates espn_api version drift."""
    return getattr(obj, name, default)


def _bye(p):
    """espn_api exposes no bye attribute; the bye is the one regular-season week absent from player.schedule."""
    weeks = {int(w) for w in (_g(p, "schedule") or {})}
    if not weeks:
        return None
    missing = [w for w in range(1, max(weeks) + 1) if w not in weeks]
    return missing[0] if len(missing) == 1 else None


def player_row(p) -> dict:
    return {
        "id": _g(p, "playerId"),
        "name": _g(p, "name"),
        "pos": _g(p, "position"),
        "nfl_team": _g(p, "proTeam"),
        "slot": _g(p, "lineupSlot"),
        "injury_status": _g(p, "injuryStatus"),
        "injured": bool(_g(p, "injured", False)),
        "bye": _bye(p),
        "proj_total": _g(p, "projected_total_points"),
        "pts_total": _g(p, "total_points"),
        "proj_week": _g(p, "projected_avg_points"),
        "pct_owned": _g(p, "percent_owned"),
    }


def team_row(t, my_team_id: int) -> dict:
    return {
        "team_id": _g(t, "team_id"),
        "name": _g(t, "team_name"),
        "is_me": _g(t, "team_id") == my_team_id,
        "wins": _g(t, "wins"),
        "losses": _g(t, "losses"),
        "points_for": _g(t, "points_for"),
        "points_against": _g(t, "points_against"),
        "standing": _g(t, "standing"),
        "waiver_rank": _g(t, "waiver_rank"),
        "roster": [player_row(p) for p in _g(t, "roster", [])],
    }


def build_state(league: League, my_team_id: int, fa_size: int) -> dict:
    week = _g(league, "current_week")
    scoreboard = []
    try:
        for m in league.scoreboard(week):
            scoreboard.append(
                {
                    "home": _g(_g(m, "home_team"), "team_name"),
                    "home_score": _g(m, "home_score"),
                    "away": _g(_g(m, "away_team"), "team_name"),
                    "away_score": _g(m, "away_score"),
                }
            )
    except Exception as exc:  # scoreboard may not exist pre-season
        scoreboard = [{"error": str(exc)}]

    free_agents = []
    try:
        free_agents = [player_row(p) for p in league.free_agents(size=fa_size)]
    except Exception as exc:
        free_agents = [{"error": str(exc)}]

    teams = [team_row(t, my_team_id) for t in _g(league, "teams", [])]
    # free-agent objects only carry the current week's schedule, so borrow the bye from a rostered teammate
    bye_by_team = {r["nfl_team"]: r["bye"] for t in teams for r in t["roster"] if r["bye"]}
    for fa in free_agents:
        if fa.get("bye") is None and fa.get("nfl_team") in bye_by_team:
            fa["bye"] = bye_by_team[fa["nfl_team"]]

    activity = []
    try:
        for a in league.recent_activity(size=25):
            activity.append(
                {
                    "date": _g(a, "date"),
                    "actions": [
                        {"team": _g(t, "team_name"), "action": act, "player": _g(p, "name")}
                        for (t, act, p, *_rest) in _g(a, "actions", [])
                    ],
                }
            )
    except Exception as exc:
        activity = [{"error": str(exc)}]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "league_id": _g(league, "league_id"),
        "season": _g(league, "year"),
        "current_week": week,
        "my_team_id": my_team_id,
        "settings": {
            "name": _g(_g(league, "settings"), "name"),
            "team_count": _g(_g(league, "settings"), "team_count"),
            "reg_season_count": _g(_g(league, "settings"), "reg_season_count"),
            "playoff_team_count": _g(_g(league, "settings"), "playoff_team_count"),
        },
        "teams": teams,
        "scoreboard": scoreboard,
        "free_agents": free_agents,
        "recent_activity": activity,
    }


def connect(league_id: int, year: int, espn_s2: str, swid: str) -> League:
    """Try cookies as pasted, then URL-decoded (DevTools often shows %-encoded espn_s2).

    Never prints cookie values. Exits with a plain message on auth failure.
    """
    from urllib.parse import unquote

    swid = swid if swid.startswith("{") else "{" + swid.strip("{}") + "}"
    attempts = [("as pasted", espn_s2), ("url-decoded", unquote(espn_s2))]
    last_err = None
    for label, s2 in attempts:
        try:
            return League(league_id=league_id, year=year, espn_s2=s2, swid=swid)
        except Exception as exc:  # espn_api raises ESPNAccessDenied / ESPNInvalidLeague
            last_err = f"{type(exc).__name__} ({label})"
    sys.exit(
        f"ESPN rejected the login: {last_err}. Re-copy espn_s2 and SWID from Chrome DevTools "
        f"(Application > Cookies > fantasy.espn.com) into bridge/.env. Cookie values were not printed."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default=str(ROOT / "state" / "league-state.json"))
    parser.add_argument("--fa-size", type=int, default=150, help="free agents to include")
    parser.add_argument("--env", default=str(HERE / ".env"))
    args = parser.parse_args()

    load_dotenv(args.env)
    required = ["ESPN_LEAGUE_ID", "ESPN_SEASON", "ESPN_TEAM_ID", "ESPN_S2", "ESPN_SWID"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        sys.exit(f"missing in {args.env}: {missing}")

    league = connect(
        int(os.environ["ESPN_LEAGUE_ID"]),
        int(os.environ["ESPN_SEASON"]),
        os.environ["ESPN_S2"],
        os.environ["ESPN_SWID"],
    )
    state = build_state(league, int(os.environ["ESPN_TEAM_ID"]), args.fa_size)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(state, indent=1, default=str), encoding="utf-8")
    me = next((t for t in state["teams"] if t["is_me"]), None)
    print(f"wrote {out} — week {state['current_week']}, {len(state['teams'])} teams, "
          f"my roster {len(me['roster']) if me else 0}, {len(state['free_agents'])} FAs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
