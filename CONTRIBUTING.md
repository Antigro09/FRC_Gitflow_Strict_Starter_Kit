# Contributing to the robot repository

> Normal contributor workflow, with the user's explicit emergency owner exception.
> GitHub rules enforce the ordinary gates. Only the configured emergency actors can
> bypass them; see [EMERGENCY_OWNER_ACCESS.md](docs/EMERGENCY_OWNER_ACCESS.md).

## 1. Branch model and ownership

`main` is the validated release line. `testing` is the protected integration branch
and fills Gitflow's `develop` role. Neither is a shared scratch branch.

```text
testing -> feature/<subsystem>/<feature-name> -> reviewed PR -> testing
testing -> release/<event-or-version> -> reviewed, validated PR -> main
main    -> hotfix/<subsystem>/<fix-name> -> reviewed, validated PR -> main
main    -> reviewed back-merge PR -> testing
```

Use actual `git flow start/publish` operations as documented in GITFLOW_COMMANDS.md.
Use lowercase kebab-case. Examples: `feature/swerve/field-centric`,
`feature/intake/auto-index`, `feature/vision/reject-stale-tags`.
Use one branch per issue/feature, not one shared long-lived branch per mechanism.
A slash is part of a Git reference name; the feature is not a folder inside testing.
The allowed subsystem list is versioned in config/ci-policy.json. Choose consistent
names rather than alternating drive/swerve or feeder/index casually. Name the issue
and responsible programmer in the PR; issue numbers in branch names are optional.

Native `git flow ... finish` merges locally and is **not** the normal way to merge
into protected branches. Finalize with a GitHub PR and **Create a merge commit**.
Keep main/testing ancestry intact; do not squash repeated release/back-merge history.

## 2. Coordinate before coding

Claim an issue and name its owner. Agree on subsystem APIs and units before editing
RobotContainer, Constants, command bindings, shared geometry, vendordeps or autonomous
assets. Coordinate dependency upgrades and broad formatting in separate PRs. Keep
feature branches short-lived and open a draft early for visibility. Explicitly agree
on ownership before multiple people push to the same feature branch.

Start from a clean tree and current testing. Fetch first, use `git pull --ff-only`,
then `git flow feature start <subsystem>/<feature-name>`. A failed fast-forward is a
signal to inspect local work, not to reset or discard it. Never force-push protected
history. Do not rebase a shared published branch without coordinated maintainer review;
the documented update procedure uses `git merge origin/testing` instead.

## 3. Commits and publication

Stage deliberately (`git add -p`; new files explicitly), inspect `git diff --cached`,
and use descriptive messages such as `feat(swerve): add field-centric control` or
`fix(vision): reject stale pose samples`. Separate unrelated work. Do not commit
credentials, generated builds or developer-local configuration. Do not replace normal
Git history with uploaded ZIP files.

Run the local checks before publishing. Push feature branches so review and server
checks can run; imperfect work may be published in a draft. **The enforced boundary
is merging into main/testing**, not a claim that every feature push is perfect.
The optional pre-push hook is convenience, can be bypassed and is not the security boundary.
An emergency owner uses an explicit one-command hook override for an authorized
direct push; the hook never silently skips checks based on ownership.

## 4. Pull requests and required gates

Use the PR template. Explain purpose, shared interfaces, exact commands/results,
robot-validation status and rollback risk. Replace placeholders; say "not run" with
a reason rather than inventing success. Use a meaningful `type(scope): description`
PR title. Ordinary feature PRs target testing; direct feature -> main is blocked by
route policy. Releases/hotfixes/main back-merges/sync branches must be same-repository.

| Requirement | Into testing | Into main |
| --- | --- | --- |
| Non-author approvals | At least 1 | At least 2 |
| Code-owner approval | Required | Required |
| Most recent reviewable push approved by someone else | Required | Required |
| Stale approval dismissal and resolved review threads | Required | Required |
| Automated status | ci-gate | ci-gate |
| Latest-base validation | Strict up-to-date; optional eligible queue | Strict up-to-date, no queue in this profile |
| Robot release gate | Honest feature-test record | robot-release-approval + release evidence |
| Merge method | Merge commit | Merge commit |

These are the ordinary contributor requirements. The emergency actors currently
configured are `Antigro09` and `Blasty25` (Soham), each with `User`/`always` bypass
on all four repository rulesets. The third intended owner's identity is pending;
no third account has been granted this exception.
An allowlisted actor can bypass reviews and required checks, including the release
check, and can merge their own PR. GitHub self-approval remains unavailable. Record
the reason and actual test results; bypass does not establish test or hardware success.

A code-owner approval can count toward the approval total; naming multiple owners on
one CODEOWNERS line does not require every named team to approve. Administrators must
configure active rules, actual authorized owners and status-check source binding.

New reviewable pushes invalidate old approvals. Do not click away unresolved technical
questions or approve your own changes. Without a merge queue, the integrator merges
one current PR at a time. When A lands, B must include the new base and rerun the
checks. Two old green results do not prove their combination works. Eligible queues
must run the same checks on merge_group; this profile queues testing only.

## 5. Strict automated checks

The Java profile requires the project to build, Java compiler warnings to be fixed,
Spotless formatting to pass, PMD to pass, JUnit reports with executed passing tests
and **no skipped tests**, plus JaCoCo coverage at the reviewed thresholds (initially
80% production lines and 70% production branches). Missing tasks/reports, zero tests,
missing measurable coverage, failures or skipped prerequisite jobs do not become a
green gate. The wrapper is validated before execution; fetched history is secret-scanned.

Meaningful regression tests must cover changed behavior and edge cases. Coverage is
not a substitute for assertions or correctness. No broad test disabling, ignoreFailures,
continue-on-error, misleading mocks or exclusions just to pass CI. Changes to workflow,
quality thresholds, suppressions, dependencies and ownership need maintainer review.
Real secrets require rotation and incident review, not only deletion from the latest file.

## 6. Resolve conflicts with intent

On the feature branch: fetch, merge origin/testing, read both changes, contact their
owners, resolve the combined behavior, stage the resolved files and commit. Run the
full local checks and push; get any renewed approvals. Never blindly choose all
"ours" or "theirs". `git merge --abort` cancels only an in-progress merge; it is not
a rollback for already-pushed history. A conflict-free textual merge can still be wrong.

## 7. Robot testing, release and competition deployment

Feature/testing/release candidates may be deployed **only in a designated supervised
practice or bench session** under the team's established robot-safety procedures.
This is necessary to validate candidates before promotion; it is not permission to
put experiments on the field. Coordinate exclusive use of the robot and record the
candidate commit/config. Never connect an untrusted CI runner to the robot network.

During competition operation, only the designated release/deploy lead loads an
approved tagged main revision. The protected robot-release-review environment adds
an authenticated human approval to main PRs; it does not measure robot behavior and
contains no automatic deploy command. A PR checkbox is not equivalent to that approval.

Record candidate commit and tree SHA, toolchain/config, test scope/results, tester,
limitations and known-good rollback version. New code/config/base changes invalidate
old evidence. Require appropriate revalidation and review for the current candidate.
After merging to main, verify its tree matches the validated candidate, identify the
release commit and create a new `comp/...` tag protected from ordinary edits/deletion.
Emergency access also bypasses tag rules; preserve release identity in normal work.
Back-merge main into testing through a reviewed merge-commit PR. Keep any active release candidate synchronized
with an approved hotfix before it can ship.

See RELEASE_CHECKLIST.md. Branch protection cannot prevent someone with robot/network
access from running `./gradlew deploy` locally; deployment station access and team
procedure are separate controls. Keep local main current and clean; record exactly
which approved version is deployed. Authorized rollback may use an older approved
tag from main history; it must not silently deploy whatever happens to be at HEAD.

## 8. Governance

Contributors own focused work; subsystem owners review behavior/interfaces; the
integrator controls merge order; release leads own test evidence and deployment;
repository maintainers activate and periodically test protections. Publish the actual
people and contact process in the repository README.

Protect main/testing from ordinary direct pushes, force pushes and deletion. Maintain
only the explicitly authorized emergency bypass actors, documented in
EMERGENCY_OWNER_ACCESS.md. Restrict who may change rules and workflow policy. Code-own the CI,
Gradle configuration, scripts, CODEOWNERS and shared robot files. An administrator who
can edit rules can still weaken them; this is a trust boundary, not an absolute guarantee.

CONTRIBUTING communicates; CODEOWNERS routes review; active GitHub rules enforce.
They must agree. Use an organization-owned required workflow when supported for a
stronger policy boundary than repository-editable workflows. Report which activation
and enforcement trials were performed; do not imply unperformed trials passed.
