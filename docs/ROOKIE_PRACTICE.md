# Rookie coding and PR practice

This is a hardware-free command robot. Pick **one** small TODO in a subsystem, add
tests for its behavior, and send a focused PR. Each shell starts with safe default
values; its comments describe the unfinished work. Coordinate changes to
`RobotContainer`, `Constants`, and commands with a mentor.

## Choose a first task

| Subsystem | Small exercise | Useful test cases |
| --- | --- | --- |
| Drive | Make `setRequestedSpeed()` store a value clamped to [-1, 1]; return it from `getRequestedSpeed()` | Initial zero, both limits, out-of-range inputs, `stop()` |
| Intake | Make `start()` set a boolean true, `stop()` set it false, and `isRunning()` return it | Initial false, start, stop, repeated calls |
| Shooter | Make `setTargetRpm()` store a value clamped to [0, 5000]; return it from `getTargetRpm()` | Initial zero, both limits, out-of-range inputs, `stop()` |
| Vision | Make `setSimulatedTargetVisible()` store its boolean and `hasTarget()` return it | Initial false, true, false again |

Follow the TODO comments and existing public methods in your selected file. Keep
units and invalid-input behavior clear. Use `Constants.Practice.MAX_SHOOTER_RPM` for
the shooter's 5000 RPM limit. Add assertions that would fail if your implementation
were wrong; executing lines alone is insufficient.

`IntakePracticeCommand` shows how a command claims a subsystem and stops it in
`end(boolean interrupted)`. Its `isFinished()` returns false, so it runs until
cancelled or interrupted by a competing command or robot disable. It has no active
controller binding. `src/test/java/frc/robot/RobotPracticeTest.java` contains baseline
HAL/scheduler examples for startup and interruption. Extend these examples or add a
test file for your subsystem's behavior; a mentor can help with desktop simulation.

## Branch, code, push, and open a PR

A mentor must first prepare `testing`, Gitflow, real owners, and strict CI using
[REPOSITORY_SETUP.md](../REPOSITORY_SETUP.md). Do not assume those settings are active
because the files exist. Start with a clean working tree and claim a task.

For an intake example, run:

```bash
git fetch origin
git switch testing
git pull --ff-only
git flow feature start intake/track-running-state
```

This creates `feature/intake/track-running-state`. Use `drive`, `intake`, `shooter`,
or `vision` for your own branch scope. Make the small change and extend the Java tests,
then run:

```bash
./gradlew spotlessApply
./gradlew test
bash tools/local-check.sh
```

On Windows PowerShell, use `.\gradlew.bat spotlessApply`, `.\gradlew.bat test`, and
`.\tools\local-check.ps1`. Desktop simulation is `./gradlew simulateJava` or
`.\gradlew.bat simulateJava`; the initial blank robot does not move mechanisms.

Inspect your changes, stage only your files, and commit. For example:

```bash
git diff
git add src/main/java/frc/robot/subsystems/intake/IntakeSubsystem.java
git add src/test/java/frc/robot/RobotPracticeTest.java
git diff --cached
git commit -m "feat(intake): track running state"
git flow feature publish intake/track-running-state
```

The example stages the existing test file; stage your own new test file instead if
you created one. Open a GitHub PR with **base
`testing`** and your feature branch as the source. Fill in every section of the PR
template: explain the change, record exact test commands/results, and state that
physical robot testing was not run for this hardware-free exercise. Ask a mentor
for review and address the comments. Final integration happens through the PR.

If a check fails, read its output and work through it with your mentor. Keep the
required coverage and checks intact. Changes to shared files, policy, dependencies,
or ownership need coordination; keep your first PR small enough to review easily.
