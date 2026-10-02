# Repository setup status — October 2, 2026

The presentation's policy is configured on the existing public repository:
https://github.com/Antigro09/FRC_Gitflow_Strict_Starter_Kit

## Branches and checks

- `main` and `testing` share the tested initial software baseline `d9644f5`.
  Existing history and the user's robot commit `8a8b50c` were retained. Initial
  maintainer bootstrap happened before protections; subsequent changes use PRs.
- Both branches require PRs, merge commits, code-owner review, fresh approvals,
  resolved review threads, and strict checks against the current base.
- `testing` requires one non-author approval and `ci-gate`.
- `main` requires two non-author approvals, `ci-gate`, and `robot-release-approval`.
- Active branch rules have empty bypass lists and block deletion/force pushes.
  Rule IDs: testing `24368649`, main `24368650`.
- Required check contexts are bound to the actual GitHub Actions app (`15368`),
  observed from a real check run. Squash and rebase merges are disabled.
- The public personal repo uses sequential integration with strict current-base
  checks. No optional merge queue is enabled.

The baseline's full hosted Robot CI succeeded on both protected lines:

- testing: https://github.com/Antigro09/FRC_Gitflow_Strict_Starter_Kit/actions/runs/37017800540
- main: https://github.com/Antigro09/FRC_Gitflow_Strict_Starter_Kit/actions/runs/37017801512

## Ownership and release review

`Antigro09` is the current administrator, initial code owner, integrator, and release
reviewer. Assign subsystem owners and additional reviewers as teammates are added.
The account cannot supply non-author approvals for its own PRs. Two other reviewers
are needed for its own main PRs under this policy.

The `robot-release-review` environment requires the initial reviewer, prevents
self-review, and has `can_admins_bypass: false`. It has no ref restriction because the
workflow itself runs only for main PRs and validates release/hotfix routes; PR merge
refs remain eligible. `RELEASE_REVIEW_CONFIGURED=true` was set after API verification.
The approval workflow has no deployment credentials and never deploys code.

`comp/**` tags cannot be updated or deleted (rule `24368652`, no bypass). A separate
creation rule (`24368654`) permits only repository administrators, currently the one
named release owner. Creation permission does not bypass tag immutability.

## Local checks and remaining validation

Java 17, git-flow-next, main/testing tracking branches, and the per-clone pre-push
guard are installed/configured. Feature updates use merge rather than rebase.
The complete local check passes with 12 JUnit tests and 55 Python policy tests;
production coverage is 94.12% lines / 100% branches against unchanged 80% / 70% gates.
The rookie subsystem TODOs remain empty.

GitHub's new PR web form was checked while signed in: the default branch's
`.github/pull_request_template.md` automatically populates its description. This
setup PR adds explicit fill-in fields while preserving the required section headings.

Actual admin direct-push attempts to both protected branches were rejected by GitHub
with GH013, even with the local hook disabled. The candidates had identical trees
to the baseline; both remote branch tips remained `d9644f5` afterward.

The first real testing PR exposed a build-validator bug: GitHub's detached PR
checkout has no local branch name. This PR fixes the Gradle configuration check to
validate Actions event metadata in CI while retaining local branch validation for
ordinary checkouts. Approval rules and all quality gates remain enforced.

The release-shaped trial PR #2 reached the protected environment on actual PR merge
refs. Its release policy passed, hardware review waited, and the pending-deployment
API reported `current_user_can_approve: false` for the initiating administrator.
The trial was closed, its waiting run cancelled, and its disposable branch removed;
no approval or merge occurred. Run:
https://github.com/Antigro09/FRC_Gitflow_Strict_Starter_Kit/actions/runs/37019166372

The setup changes remain reviewable in PR #1:
https://github.com/Antigro09/FRC_Gitflow_Strict_Starter_Kit/pull/1
Ordinary-writer/stale-approval trials require real teammate accounts. No physical robot
validation, competition tag, or competition-ready release is claimed. Team number
remains the placeholder `0`, to be set before supervised hardware work.
