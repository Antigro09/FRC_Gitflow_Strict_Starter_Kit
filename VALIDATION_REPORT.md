# Validation report

Prepared September 24, 2026. This separates local artifact checks from real robot/hosted checks.

## Executed successfully in the working environment

- **55 Python unit tests passed**, including valid/invalid branch names and PR
  routes; same-repository release restrictions; configuration and PR-body validation;
  missing/zero/skipped/failing JUnit results; coverage boundaries and missing counters;
  and actual final-gate scripts rejecting failure, skipped, cancelled and missing jobs.
- **4 real local Git preflight scenarios passed:** an annotated approved-tag checkout
  accepted; untracked changes rejected; wrong checked-out branch rejected; mismatched
  tagged/current revision rejected. These used a disposable local synthetic repository.
- Both workflow YAML files parsed; every third-party action reference is a full
  40-character SHA. Read-only token permissions, main-only release events, testing
  merge_group support and explicit fail-closed final dependencies were inspected.
- **14 shell scripts/embedded shell steps** passed `bash -n`; **3
  embedded Python scripts** and all shipped Python files passed syntax parsing.
- All supplied JSON and PMD XML parsed. Ruleset fields were compared with current
  official GitHub schema documentation; no live import has been performed.
- The unconfigured starter was deliberately rejected by the policy CLI as intended.
- Gitleaks Linux x64 checksum and action commit pins were checked against official
  upstream release metadata. Downloaded tooling was not executed in this environment.

## Presentation checks

The 32-slide editable PowerPoint was built from the newly attached Keynote file,
not the previous PowerPoint. All slides were rendered and visually inspected.
All 32 slides have speaker notes; hyperlinks and the original proposal form were
preserved. Shape bounds and the PPTX archive were checked. The original Keynote
file was left unchanged; no native .key output is claimed.

## Not executed, and still required before adoption

No real robot repository/source, Gradle wrapper, dependency graph or tests were supplied.
Therefore **no WPILib compilation, Gradle ciVerify, PMD/Spotless execution, real JUnit
suite, real coverage measurement, full Gitleaks scan, hosted Actions run, git-flow-next
CLI execution, GitHub ruleset import, environment approval, merge queue, or robot test**
is claimed. The PowerShell script was inspected but not executed on Windows.

The documented image is WPILib's current 2026 CI choice; its digest remains an admin
verification/pinning step. Pinned Java analyzer versions require confirmation against
the team's actual season toolchain. This kit is a reviewed, locally tested integration
starting point—not a production certification or a guarantee of perfect code.

Complete docs/BUILD_INTEGRATION.md, then the deliberate negative tests in
REPOSITORY_SETUP.md, before calling these gates active. Repository-editable workflows
and administrator-controlled rules remain trust boundaries; code review and real
hardware validation cannot be replaced by a green indicator.
