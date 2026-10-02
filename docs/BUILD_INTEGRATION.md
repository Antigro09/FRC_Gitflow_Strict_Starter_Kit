# Integrate with the actual WPILib project

This kit targets a **single-project Java robot using a Groovy `build.gradle`**.
It is not a robot project and does not contain GradleRIO, the Gradle wrapper, JUnit
libraries, vendor libraries, robot code, or fabricated tests. Do not replace your
existing build.gradle. C++, Kotlin DSL, and multi-project repositories need a reviewed
language/project-specific adapter; the kit deliberately does not claim to validate them.

## Required edits

Add this one line inside your existing root `plugins { ... }` block, alongside Java
and your season's GradleRIO plugin. If Spotless already exists, retain a tested,
compatible pinned version instead of declaring it twice:

```groovy
id 'com.diffplug.spotless' version '6.25.0'
```

Add this at the bottom, after the project's normal WPILib/native-test configuration:

```groovy
apply from: 'gradle/quality.gradle'
```

Retain the robot project's Java toolchain (normally Java 17 for this profile), Gradle
wrapper and `wpi.java.configureTestTasks(test)` setup. Ensure JUnit Jupiter dependencies
are actually configured in the original project. Do not bypass HAL initialization
when tests need it; separate pure control/geometry logic from hardware I/O so it can
be tested deterministically. Add real tests under `src/test/java`.

In `config/ci-policy.json`, choose the subsystem vocabulary, review coverage defaults,
and set `configured` to `true` only after integration. Replace all CODEOWNERS placeholders.
Resolve formatting with `./gradlew spotlessApply`, inspect the diff, then run:

```bash
bash tools/local-check.sh
```

The local script runs policy/unit checks, a clean `ciVerify`, then XML report checks.
The Actions job also validates the wrapper and scans secrets. Missing Gradle tasks,
missing/zero/skipped tests, insufficient coverage, and warnings are failures, not skips.
`minimum_executed_tests: 1` only prevents an empty suite; it is not a sufficient test plan.

## Quality policy

The starting thresholds are **80% production line coverage and 70% production branch
coverage**, with no default production exclusions. They are team-chosen review gates,
not evidence of correctness. Add edge cases for angle wraparound, sensor dropout,
command interruption, unit conversion and actuator limits. A suite that merely executes
lines without assertions is inadequate even when coverage is high.

Compiler `-Xlint:all -Werror` makes Java warnings fatal. New-season/vendor deprecations may
need real fixes or a narrowly documented, reviewed suppression. PMD failures are fatal.
Never silently lower thresholds, exclude hard-to-test subsystems or add broad suppressions
to turn the indicator green. Quality configuration is code-owned.

Spotless 6.25.0, Google Java Format 1.17.0, PMD 7.10.0 and JaCoCo 0.8.12 are explicit
compatibility-oriented pins, not a claim that they are the newest versions. Validate
them against your actual season wrapper and update deliberately in a separate PR.
The example CI container is the image WPILib currently documents for 2026:
`wpilib/roborio-cross-ubuntu:2025-22.04`. Do not invent a 2026 tag. Administrators should
also record/pin a verified image digest after pulling and validating that image.

## Preserve existing files

Merge .gitattributes/.editorconfig/CODEOWNERS content instead of overwriting local rules.
Review any line-ending normalization in a dedicated PR. Keep the existing .gitignore;
exclude build/, .gradle/, __pycache__/ and developer-local files as appropriate, but
never ignore robot source, vendordeps, or required deploy assets.
