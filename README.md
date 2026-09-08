# fantasy-football — Claude-managed season (2026)

League: Snipes and Degens (ESPN, 10-team, 0.5 PPR). Team: Ryan Lost the Championship (teamId 5).
Purpose: run the season with Claude as manager, log everything, and produce a post-season article on
(a) where Claude was effective, (b) where a human was necessary, (c) what the experience was like, and
(d) a transferable framework — the context, models, and techniques — that lets a reader make their own Claude
maximally effective.

## Layout
```
README.md                 this file
STANDING-ANSWERS.md       confirmed decisions that govern every routine (never re-asked)
context-package.md        the framework: what context to give a Claude for this job (article deliverable)
playbook.md               evolving lessons; updated every Monday by the outcome routine
schema/DECISION-LOG.md    field spec for the .jsonl logs
schema/validate.py        validator (python schema/validate.py logs/decisions.jsonl)
tests/test_validate.py    pytest
logs/decisions.jsonl      canonical decision log — one line per recommendation (draft, waiver, lineup, trade)
logs/sessions.jsonl       one line per Claude session: model, tools, failures, latency
logs/weekly/W##.md        Monday summaries (Markdown, derived from the .jsonl)
state/league-state.json   published nightly by bridge/espn_state.py (rosters, waivers, scores)
bridge/                   local script + setup that publishes league state to this public repo
routines/                 the four scheduled-task prompts, versioned so technique changes are visible
2026-draft-*.md           draft-night artifacts (strategy v1/v2, sleepers, recap)
```

## Data flow
```
ESPN (private league) --espn_api + your cookies (local .env)--> bridge/espn_state.py
   --> state/league-state.json --git push--> public GitHub raw URL
   --> cloud scheduled routine (Tue/Thu/Sun/Mon) reads it + web research
   --> proposal pushed to your phone + logged to Google Drive (.jsonl)
   --> you approve --> Chrome submits (desktop linked) OR you submit in ESPN app (<12h rule)
   --> Monday routine scores outcomes, updates playbook.md, writes logs/weekly/W##.md
   --> desktop-linked session syncs Drive logs into logs/ and commits
```

## Grading baselines (all three logged per decision)
1. Hindsight-optimal — best available choice once results are in (isolates Claude error)
2. ESPN projection / autopick — the free baseline (did Claude beat the default?)
3. League outcome — W/L, points for, standings, playoff result

Plus: Claude recommendation vs. human action (isolates user error / user override).

## Commands
```
python -m pip install -r bridge/requirements.txt
python bridge/espn_state.py            # writes state/league-state.json
python schema/validate.py logs/decisions.jsonl logs/sessions.jsonl
python -m pytest tests -q
```
