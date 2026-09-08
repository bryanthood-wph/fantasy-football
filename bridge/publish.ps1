# Nightly: refresh league state and push to GitHub. Run from any cwd by Task Scheduler.
# Logs to bridge/publish.log (git-ignored). Never prints cookie values.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root
$log = Join-Path $root "bridge/publish.log"
"---- $(Get-Date -Format s)" | Out-File -Append -Encoding utf8 $log

# Resolve a Python that actually has our dependencies installed — not just "a real,
# non-Store python". This machine has multiple installs (e.g. Anaconda's python.exe
# resolves ahead of the Python.org one on PATH for a freshly spawned process, which is
# exactly how Task Scheduler launches this script), so check the required imports rather
# than just checking sys.executable.
$pyCmd = $null
$pyArgs = @()
$candidates = @(
  @{ Cmd = "python"; Args = @() },
  @{ Cmd = "py"; Args = @("-3.11") },
  @{ Cmd = "py"; Args = @("-3") },
  @{ Cmd = "py"; Args = @() }
)
foreach ($c in $candidates) {
  try {
    $exe = (& $c.Cmd @($c.Args) -c "import sys, dotenv, espn_api; print(sys.executable)" 2>$null)
    if ($LASTEXITCODE -eq 0 -and $exe -and ($exe -notmatch "WindowsApps")) { $pyCmd = $c.Cmd; $pyArgs = $c.Args; break }
  } catch {}
}
if (-not $pyCmd) { "no python with required packages found (dotenv, espn_api) - run: pip install -r bridge/requirements.txt" | Out-File -Append -Encoding utf8 $log; exit 1 }

try {
  & $pyCmd @pyArgs bridge/espn_state.py 2>&1 | Out-File -Append -Encoding utf8 $log
  if ($LASTEXITCODE -ne 0) { throw "espn_state.py exited $LASTEXITCODE" }
  # Drain cloud-run logs from the Drive inbox. A bad inbox line must not block the state publish,
  # and sync_logs.py writes nothing on failure, so just record it and carry on.
  & $pyCmd @pyArgs bridge/sync_logs.py 2>&1 | Out-File -Append -Encoding utf8 $log
  if ($LASTEXITCODE -ne 0) { "sync_logs.py exited $LASTEXITCODE - inbox left untouched, state still publishes" | Out-File -Append -Encoding utf8 $log }
  git add state/league-state.json logs playbook.md
  $changed = git status --porcelain state/league-state.json logs playbook.md
  if ($changed) {
    # git writes normal progress to stderr; PS 5.1 wraps piped stderr lines as terminating
    # errors under $ErrorActionPreference = "Stop" even on success, so relax it for these calls.
    $ErrorActionPreference = "Continue"
    git commit -m "state: $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>&1 | Out-File -Append -Encoding utf8 $log
    git push 2>&1 | Out-File -Append -Encoding utf8 $log
    $pushExit = $LASTEXITCODE
    $ErrorActionPreference = "Stop"
    if ($pushExit -ne 0) { throw "git push failed" }
  } else { "no change" | Out-File -Append -Encoding utf8 $log }
  "ok" | Out-File -Append -Encoding utf8 $log
} catch { "ERROR: $_" | Out-File -Append -Encoding utf8 $log; exit 1 }
