# Bridge setup (one time, ~15 minutes, Windows)

Goal: your PC publishes `state/league-state.json` to a public GitHub repo every night so the cloud routines can read your
private league without your login. Your cookies stay in `bridge/.env` on this machine. Claude never sees them.

## 1. Create the public repo
1. github.com → New repository → name `fantasy-football`, **Public**, no README (the folder already has one).
2. In PowerShell:
   ```powershell
   cd C:\github\fantasy-football
   git init
   git add .
   git commit -m "season 2026: documentation system"
   git branch -M main
   git remote add origin https://github.com/<your-username>/fantasy-football.git
   git push -u origin main
   ```
   `.gitignore` already excludes `bridge/.env` and `bridge/publish.log`. Verify with `git status` that `.env` is not listed.

## 2. Get your two ESPN cookies (do this yourself — do not paste them into Claude)
1. In Chrome, log in to fantasy.espn.com.
2. Press F12 → Application tab → Storage → Cookies → `https://fantasy.espn.com`.
3. Copy the value of `espn_s2` (long string) and `SWID` (looks like `{XXXXXXXX-XXXX-...}`, keep the braces).
4. Copy `bridge\.env.example` to `bridge\.env` and paste the values in. Cookies typically last months; if the script starts
   failing with 401, repeat this step.

## 3. Install and test
```powershell
python -m pip install -r bridge\requirements.txt
python bridge\espn_state.py
```
Expected: `wrote C:\github\fantasy-football\state\league-state.json — week N, 10 teams, my roster 16, 150 FAs`.
Open the file and confirm your roster is there. Then:
```powershell
powershell -ExecutionPolicy Bypass -File bridge\publish.ps1
```
This commits and pushes the state file. Check `bridge\publish.log` if anything looks off.

## 4. Schedule it (twice daily)
Two tasks, created from an elevated PowerShell (schtasks takes one trigger per task):
```powershell
$act = 'powershell.exe -ExecutionPolicy Bypass -File "C:\github\fantasy-football\bridge\publish.ps1"'
schtasks /Create /TN ff-publish-state-am /SC DAILY /ST 05:30 /TR $act /IT /F
schtasks /Create /TN ff-publish-state-pm /SC DAILY /ST 18:30 /TR $act /IT /F
schtasks /Run /TN ff-publish-state-am
Get-Content bridge\publish.log -Tail 5
```
`/IT` = "run only when user is logged on" — it runs while the PC is **locked**, not when signed out or off. That mode needs no
password and keeps your Git credentials available to the job. If you want it to run while signed out, open Task Scheduler, edit
each task, and choose "Run whether user is logged on or not" — Windows itself will ask for your password there (never type it
into Claude). Either way the PC must be on; the cloud routines fall back to the last published state and say how stale it is.
Also untick "Start only if on AC power" and tick "Run task as soon as possible after a scheduled start is missed".

## 5. Tell Claude the raw URL
Send Claude: `https://raw.githubusercontent.com/<your-username>/fantasy-football/main/state/league-state.json`.
Claude writes it into `config.json` in the Google Drive log folder; every routine reads it from there.

## Rotating or revoking
Log out of ESPN in Chrome and back in → new cookies → update `.env`. Deleting `.env` disables the bridge; routines keep working
from the last published state.
