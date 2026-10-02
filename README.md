# FRC Java robot + strict Gitflow starter kit

This folder includes a **2026 WPILib Java command-based robot project** and the team's
Gitflow/review policy from the presentation, with the user's explicit emergency
owner exception. The repository is [BlueCheese1086/GitHub-Etiquette-Repo](https://github.com/BlueCheese1086/GitHub-Etiquette-Repo).
It uses Java 17, GradleRIO 2026.2.1, and the Gradle 8.11
wrapper, with the WPILib command library and JUnit test configuration.

The robot starts empty: `Robot` runs the command scheduler, `RobotContainer` owns
the subsystems, and autonomous returns a do-nothing command. Drive, intake, shooter, and vision
are hardware-free starter shells with small commented exercises. An intake practice
command demonstrates subsystem requirements and cleanup when interrupted. No
controller bindings are active, and no motor controllers are created.

## Open and run

Install the 2026 WPILib tools, then open **this entire folder** in WPILib VS Code
(File → Open Folder). Open the integrated terminal at the project root.

| Action | macOS / Linux | Windows PowerShell |
| --- | --- | --- |
| Build | `./gradlew build` | `.\gradlew.bat build` |
| Run Java tests | `./gradlew test` | `.\gradlew.bat test` |
| Open desktop simulation | `./gradlew simulateJava` | `.\gradlew.bat simulateJava` |
| Apply Java formatting | `./gradlew spotlessApply` | `.\gradlew.bat spotlessApply` |

The first build downloads dependencies. Simulation starts a blank robot and the
simulation GUI; add exercise behavior before expecting a mechanism to do anything.
The team number is deliberately **0** in `.wpilib/wpilib_preferences.json`. Set the
real number before any supervised deployment. These practice shells do not represent
a configured physical robot.

Start with [the rookie exercises](docs/ROOKIE_PRACTICE.md). Read
[CONTRIBUTING.md](CONTRIBUTING.md) and [GITFLOW_COMMANDS.md](GITFLOW_COMMANDS.md) for
branch, push, and PR rules.

## Repository workflow

1. Follow [docs/BUILD_INTEGRATION.md](docs/BUILD_INTEGRATION.md): choose real owners,
   configure the strict policy, and satisfy the quality checks.
2. Follow [REPOSITORY_SETUP.md](REPOSITORY_SETUP.md): create the `testing` integration
   branch, activate GitHub rules and release review, and run the negative checks.
3. Have rookies use `feature/<subsystem>/<task>` branches and open PRs into `testing`.
   GitHub PRs authorize merges; local `git flow finish` does not.

The Java CI policy is configured, with `@Antigro09` as the initial code owner.
`ciVerify` validates ownership, builds, tests, formatting, static checks and coverage.
Missing tests, skipped tests or inadequate coverage block the strict gate. The starting thresholds are
80% production line coverage and 70% branch coverage. Do not lower them or hide code
to make exercise PRs green; add meaningful tests and review the result with a mentor.

The initial code owner and release reviewer is `@Antigro09`. The normal workflow
requires non-author reviews; the explicit emergency allowlist currently contains
`Antigro09` and `Blasty25` (Soham), each with `User`/`always` bypass on all four
repository rulesets. Both can bypass PR/check requirements and push directly.
The third intended owner's identity is pending and has not been granted this exception.
GitHub still disallows self-approval.
The protected release environment prevents self-review and never deploys code.
See [emergency owner access](docs/EMERGENCY_OWNER_ACCESS.md) for the exact exception,
local push command and organization limitations.
See [local setup](docs/LOCAL_SETUP.md) for clone configuration and tool commands.

## Files to know

| Location | Purpose |
| --- | --- |
| `src/main/java/frc/robot/` | Robot lifecycle, container, constants, commands, and subsystem exercises |
| `src/test/java/` | Java tests to run and extend |
| `src/main/deploy/` | Files packaged for deployment |
| `build.gradle`, `vendordeps/`, `gradle/wrapper/` | WPILib build and required dependencies |
| `docs/ROOKIE_PRACTICE.md` | Small exercises and a branch-to-PR walkthrough |
| `.github/`, `config/`, `gradle/quality.gradle` | Strict review and automated quality setup |
| `tools/` | Policy/report validators and local checks |
| `RELEASE_CHECKLIST.md` | Release evidence and competition procedure |
| `VALIDATION_REPORT.md`, `SOURCES.md` | Recorded checks, limitations, and dependency sources |
