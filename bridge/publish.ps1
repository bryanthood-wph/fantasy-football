# Nightly: refresh league state and push to GitHub. Run from any cwd by Task Scheduler.
# Logs to bridge/publish.log (git-ignored). Never prints cookie values.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root
$log = Join-Path $root "bridge/publish.log"
"---- $(Get-Date -Format s)" | Out-File -Append -Encoding utf8 $log

# Resolve a real Python (skip the Microsoft Store stub).
$py = $null
foreach ($cand in @("python", "py")) {
  try {
    $exe = (& $cand -c "import sys; print(sys.executable)" 2>$null)
    if ($LASTEXITCODE -eq 0 -and $exe -and ($exe -notmatch "WindowsApps")) { $py = $cand; break }
  } catch {}
}
if (-not $py) { "no working python found" | Out-File -Append -Encoding utf8 $log; exit 1 }

try {
  if ($py -eq "py") { & py -3 bridge/espn_state.py 2>&1 | Out-File -Append -Encoding utf8 $log }
  else { & python bridge/espn_state.py 2>&1 | Out-File -Append -Encoding utf8 $log }
  if ($LASTEXITCODE -ne 0) { throw "espn_state.py exited $LASTEXITCODE" }
  git add state/league-state.json
  $changed = git status --porcelain state/league-state.json
  if ($changed) {
    git commit -m "state: $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>&1 | Out-File -Append -Encoding utf8 $log
    git push 2>&1 | Out-File -Append -Encoding utf8 $log
    if ($LASTEXITCODE -ne 0) { throw "git push failed" }
  } else { "no change" | Out-File -Append -Encoding utf8 $log }
  "ok" | Out-File -Append -Encoding utf8 $log
} catch { "ERROR: $_" | Out-File -Append -Encoding utf8 $log; exit 1 }
