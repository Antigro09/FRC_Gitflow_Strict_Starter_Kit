$ErrorActionPreference = 'Stop'
function Assert-Exit([string]$Step) {
    if ($LASTEXITCODE -ne 0) { throw "$Step failed (exit $LASTEXITCODE)." }
}
$Root = git rev-parse --show-toplevel
Assert-Exit 'Locate repository'
Set-Location $Root
python tools/ci_policy.py --local
Assert-Exit 'Policy'
python -m unittest discover -s tools/tests -v
Assert-Exit 'Policy unit tests'
git diff --check
Assert-Exit 'Working-tree whitespace'
git diff --cached --check
Assert-Exit 'Staged whitespace'
& .\gradlew.bat --no-daemon --stacktrace clean ciVerify
Assert-Exit 'Robot quality checks'
python tools/verify_reports.py
Assert-Exit 'Reports'
Write-Host 'Local checks passed. Server wrapper validation, secret scan and reviews still apply.'
