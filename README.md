# FRC Gitflow + strict review starter kit

**Prepared September 24, 2026.** This is a proposed team policy and integration kit,
not an already-enforced repository or a certified robot build. Start here before copying files.

## What this changes

Use real `git flow` commands to create/publish short-lived branches named
`feature/<subsystem>/<feature-name>`. Keep `testing` as Gitflow's integration/develop
branch and `main` as the validated release line. GitHub PRs, not local `git flow finish`,
authorize merges into those protected branches. There is one explicit integration order.

The Java CI profile builds the robot, rejects compiler warnings, checks formatting,
runs PMD, requires executed passing tests with no skips, enforces 80% line / 70% branch
coverage, validates the Gradle wrapper, and scans fetched Git history for secrets.
A fail-closed `ci-gate` blocks merge unless every prerequisite succeeds. A separate
main-PR-only approval workflow supports an authenticated release-lead review.

**A green result is evidence, not perfection.** Coverage can be gamed; sensors, wiring,
configuration, timing and real-world behavior still need appropriate validation.
Actions run after feature pushes. They block protected merges once the rules are
activated; they do not stop every broken feature commit from reaching GitHub.

## Install in this order

1. Preserve your robot project's files. Merge this kit through a dedicated reviewed
   setup branch; do not overwrite an existing CONTRIBUTING, CODEOWNERS or build file.
2. Follow **docs/BUILD_INTEGRATION.md**. This profile is for **Java + Groovy Gradle,
   single-project WPILib**. Configure real tests/owners, review thresholds, and set
   `config/ci-policy.json` → `configured: true` only when integrated.
3. Run the local checks. Resolve all genuine failures; do not suppress the jobs to pass.
4. Follow **REPOSITORY_SETUP.md** to activate rules, bind real Actions check sources,
   create the protected approval environment, and run deliberate failing-PR tests.
5. Teach **CONTRIBUTING.md** and **GITFLOW_COMMANDS.md**. Use the release checklist
   before any competition deployment.

Both `configured: false` and an unset `RELEASE_REVIEW_CONFIGURED` are intentional
fail-closed defaults. Merely copying the files should NOT give an unconfigured robot
a misleading green badge. No live repository settings were changed by creating this kit.

## Files

| Location | Purpose |
| --- | --- |
| CONTRIBUTING.md | Team-facing work/review/release policy |
| GITFLOW_COMMANDS.md | Actual start/publish commands; PR-safe finalization |
| .github/workflows/robot-ci.yml | Strict automated candidate checks |
| .github/workflows/release-review.yml | Main-only protected approval; no deployment |
| .github/rulesets/*.json | Importable ruleset templates; administrator setup required |
| .github/CODEOWNERS | Replace placeholders with authorized real teams |
| gradle/quality.gradle, config/ | Java build/format/static/test/coverage settings |
| tools/ | Validators, local checks, optional hook and deployment preflight |
| tools/tests/ | Local unit tests of the kit's policy/report/preflight logic |
| RELEASE_CHECKLIST.md | Evidence, exact revisions and competition procedure |
| VALIDATION_REPORT.md | What was actually checked and what was not run |
| SOURCES.md | Official technical references and dependency pins |

The integration steps may initially expose substantial missing test coverage. Treat
that as work to do before adopting the strict baseline, not permission to claim an
empty test suite proved the robot correct. A policy change needs explicit maintainer review.
