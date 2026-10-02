# Validation report — Java robot addition

Validated October 2, 2026, on macOS arm64 with Java 17 and the pinned Gradle 8.11
wrapper. A checksum-verified JDK was used from a temporary workspace directory;
no system Java installation was changed. WPILib tools/Java are not bundled in the
source ZIP. Install the 2026 WPILib tools for normal editor/build/simulation use.

## Passed for the added project

- `./gradlew --no-daemon build spotlessCheck pmdMain pmdTest jacocoTestReport`.
  Both production and test compilation retain `-Xlint:all -Werror`.
- **6 JUnit tests executed, 0 failures, 0 errors, 0 skips.** These test safe initial
  subsystem defaults, intake requirements and one-time start, cancellation cleanup,
  competing-command interruption, disable cleanup, and empty autonomous completion.
  HAL and Driver Station simulation ran with desktop native libraries.
- **55 Python policy/report tests passed** using the bundled Python runtime.
- Gradle wrapper JAR hash matched Gradle's official published checksum; the Gradle
  distribution hash is pinned in the wrapper configuration.
- WPILib preferences, VS Code configuration, and the command vendordep parsed as JSON.
- Built robot JAR contains `Main-Class: frc.robot.Main`, the robot classes, and the
  WPILib command library. `git diff --check` and shell syntax checks passed.
- `simulateJava --dry-run` resolved the desktop simulation task graph. The interactive
  simulation GUI was not launched during this validation.

## Strict gate status: not ready

`./gradlew --no-daemon ciVerify` was deliberately rejected at
`verifyCiConfiguration`: the shipped policy is still `configured: false`.
Placeholder CODEOWNERS remain for mentors to replace. Ordinary build/test/simulation
are available without claiming that strict repository setup is complete.

Measured starter production coverage is **30/70 lines (42.86%)** and **0/4 branches
(0%)**, below the unchanged 80% line / 70% branch thresholds. The tests are a small
command/testing example; they do not validate unfinished exercise behavior or the
full robot lifecycle. Add meaningful behavior and lifecycle tests before adopting
the strict baseline. No exclusions, warning suppressions, or reduced thresholds
were added to force a passing indicator.

## Not performed in this addition

No physical robot/deployment test, Windows execution, Linux/container execution,
full secret-history scan, hosted Actions run, GitHub ruleset/environment changes,
remote pushes, or PR creation was performed. Team number remains the explicit
placeholder `0`. Configure real owners, team details, tests, and protections using
`docs/BUILD_INTEGRATION.md` and `REPOSITORY_SETUP.md` before adoption.

---

## Historical September 24 kit validation

The following original report is preserved as the earlier kit-only snapshot. Its
statements about absent Java source/wrappers predate this addition; the current
project results and remaining limits are recorded above.


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
