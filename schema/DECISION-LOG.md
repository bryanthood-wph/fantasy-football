# Log schema

Two append-only `.jsonl` files. One JSON object per line. Validate with `python schema/validate.py <file>`.

## logs/decisions.jsonl — one line per recommendation

| Field | Type | Required | Meaning |
|---|---|---|---|
| `id` | string | yes | `YYYY-Www-NNN` (draft night = `2026-W00-NNN`) |
| `ts` | ISO-8601 | yes | when the recommendation was made |
| `week` | int | yes | NFL week; 0 = draft |
| `phase` | enum | yes | `draft` `waiver` `lineup` `trade` `stream` |
| `slot` | string | no | roster slot or pick number (`R1P5`, `FLEX`, `K`) |
| `deadline` | ISO-8601 | no | the deadline the decision faced |
| `claude_rec` | object | yes | see below |
| `baselines` | object | yes | `espn_projection_choice`, `espn_autopick`, `espn_rank_of_rec` |
| `human_action` | object | yes | `choice`, `followed` (`yes`/`partial`/`no`), `override_reason`, `submitted_by` (`claude`/`human`/`autopick`) |
| `outcome` | object | later | `hindsight_optimal`, `pts_rec`, `pts_action`, `pts_optimal`, `pts_espn_choice`, `scored_at` |
| `technique` | object | yes | `model`, `session_type` (`live`/`scheduled`/`desktop-linked`), `prompt_pattern`, `tools`, `time_to_decision_s`, `failures` |
| `article` | object | yes | `category`, `anecdote` (bool), `note` |
| `context_ref` | string | no | pointer to state snapshot (`state/league-state.json@<sha>` or file) |

### `claude_rec`
```
{ "choice": "Derrick Henry", "alternatives": ["Amon-Ra St. Brown"], "confidence": 0.7,
  "reasoning": "...", "lens": {"age": "...", "injury": "...", "opportunity": "...", "bye": "...", "tier_gap": "..."},
  "sources": ["ESPN draft board 2026 proj", "https://..."] }
```

### `article.category` (one)
`claude_win` — rec followed and beat both baselines
`claude_miss` — rec followed and lost to hindsight-optimal by a material margin
`human_win` — override beat Claude's rec
`human_error` — override lost to Claude's rec
`tooling_limit` — the decision was shaped by a tool/latency/access failure
`tie` — no material difference
`pending` — not yet scored

## logs/sessions.jsonl — one line per Claude session that touched the team

| Field | Meaning |
|---|---|
| `id` | `S-YYYYMMDD-NN` |
| `ts_start`, `ts_end` | |
| `model` | model id actually serving (note switches) |
| `surface` | `cowork-live` / `scheduled` / `chrome-side-panel` |
| `tools` | list, e.g. `claude-in-chrome.get_page_text`, `WebSearch`, `Agent` |
| `decisions` | list of decision ids produced |
| `failures` | list of `{what, impact, workaround}` |
| `latency_notes` | free text: clock pressure, seconds per read |
| `technique_changes` | what was tried differently vs. last session |
| `human_notes` | Colby's optional one-liner on the experience |

## Scoring rules (Monday routine)
- `pts_*` = actual fantasy points in this league's scoring for the relevant week(s). For draft picks, season-to-date points through the scoring date, re-scored each Monday.
- `hindsight_optimal` = the best player available at that moment at the same position(s), by actual points.
- Material margin = ≥ 3.0 points for a single-week lineup decision; ≥ 15.0 season points for a draft/waiver decision.
