# WPILib build and strict CI setup

This kit now includes a **single-project 2026 WPILib Java robot using Groovy
`build.gradle` and Java 17**. GradleRIO 2026.2.1, the Gradle 8.11 wrapper, WPILib commands,
JUnit, native test configuration, and `gradle/quality.gradle` are already connected. Open the whole
folder in WPILib VS Code; do not create a second robot project inside it.

## Build, test, and simulate

Use the integrated terminal at the project root:

```bash
./gradlew build
./gradlew test
./gradlew simulateJava
```

In Windows PowerShell, use `.\gradlew.bat build`, `.\gradlew.bat test`, and
`.\gradlew.bat simulateJava`. These commands are available before strict repository
policy is configured. Simulation is a hardware-free starting point with no active
controller bindings. Set the real team number in `.wpilib/wpilib_preferences.json`
(currently `0`) before supervised deployment.

## Activate the strict profile

1. Replace every `.github/CODEOWNERS` placeholder with an authorized real owner.
2. Review the subsystem vocabulary and thresholds in `config/ci-policy.json`; set
   `configured` to `true` when the repository is actually ready.
3. Add meaningful tests for implemented behavior, including command interruption
   and cleanup. HAL-dependent tests need HAL initialization; pure control logic can
   be tested separately from hardware I/O.
4. Apply formatting, inspect the changes, then run the full local checks:

```bash
./gradlew spotlessApply
bash tools/local-check.sh
```

Windows PowerShell:

```powershell
.\gradlew.bat spotlessApply
.\tools\local-check.ps1
```

`ciVerify` validates policy and owners before accepting the strict build. The local
script also checks branch naming, runs the Python validator tests, and verifies JUnit
and JaCoCo XML reports. Actions additionally validate the wrapper and scan fetched
history for secrets. This repository now has `configured: true` and a real initial owner, `@Antigro09`.
Copies of the kit must configure their own owners and protections; a passing local
build does not activate remote rules.

Follow [REPOSITORY_SETUP.md](../REPOSITORY_SETUP.md) to activate rules and create the
`testing` integration branch before using these gates for rookie PRs. Build/test
success alone does not prove that GitHub protections are active.

## Quality requirements

The starting thresholds are **80% production line coverage and 70% production branch
coverage**, with no default production exclusions. Tests must execute and pass with
no skips; zero tests, missing reports, or missing measurable coverage fail the gate.
`minimum_executed_tests: 1` is an empty-suite guard, not a sufficient test plan.

Java compiler warnings are fatal (`-Xlint:all -Werror`), formatting must pass, and PMD
findings must be resolved. Do not lower coverage, disable tests, or add broad exclusions
and suppressions to turn the indicator green. Test observable results and edge cases
such as invalid inputs, actuator limits, sensor dropout, and command interruption.

Spotless 6.25.0, Google Java Format 1.17.0, PMD 7.10.0, and JaCoCo 0.8.12 are explicit
pins. Dependency changes need deliberate review. The CI container remains
`wpilib/roborio-cross-ubuntu:2025-22.04`, the documented image for the 2026 profile;
administrators should verify and pin a pulled image digest.

## Reusing this in another robot repository

Preserve the existing robot project's build, vendor dependencies, tests, and local
rules. Merge this setup through a reviewed branch rather than overwriting files.
The build needs Spotless in the root plugin block and this line after normal WPILib
configuration:

```groovy
apply from: 'gradle/quality.gradle'
```

Retain `wpi.java.configureTestTasks(test)` and the season's toolchain/native setup.
Merge `.gitattributes`, `.editorconfig`, `.gitignore`, and CODEOWNERS rules carefully;
keep robot source, vendordeps, wrapper files, and required deploy assets tracked.
C++, Kotlin DSL, and multi-project builds require an appropriate reviewed adapter.
