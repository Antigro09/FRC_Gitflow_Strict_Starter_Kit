# Gitflow commands for this team

## One-time setup per clone

These commands target **git-flow-next**. Install with `brew install gittower/tap/git-flow-next`
on macOS/Linux (Homebrew), or `winget install GitTower.GitFlowNext` on Windows.
Run `git flow version` and confirm you installed the intended implementation.
Older git-flow/AVH variants have different flags; do not assume identical behavior.

The maintainer must first establish remote `main` and `testing`. From a clean clone,
fetch and check that both exist; create local tracking branches only when missing.

```bash
git fetch origin
git branch -a
git flow init --preset=classic --defaults --main=main --develop=testing --feature=feature/ --release=release/ --hotfix=hotfix/
```

Interactive `git flow init` is also valid: explicitly choose **main**, **testing** and
**feature/**. Do not accidentally accept `develop` or `master`. Configuration is per
clone; do not use `--force` to overwrite someone's existing setup without reviewing it.

## Normal feature: from testing to a reviewed PR

```bash
git status
git fetch origin
git switch testing
git pull --ff-only origin testing
git flow feature start swerve/field-centric
# Work on feature/swerve/field-centric.
git add -p
# Add genuinely new files explicitly: git add <actual-path>
git diff --cached
git commit -m "feat(swerve): add field-centric control"
bash tools/local-check.sh
git flow feature publish swerve/field-centric
```

Open a GitHub PR: **base `testing`**, compare `feature/swerve/field-centric`.
On Windows, use `tools/local-check.ps1` with Python available. For later updates,
commit normally and `git push`; `publish` is the initial remote publication step.

To incorporate newly integrated work, start clean and stay on the feature branch:

```bash
git fetch origin
git merge origin/testing
# If there are conflicts, resolve them with the other author, then git add / git commit.
bash tools/local-check.sh
git push
```

Do not blindly use `git flow feature update`: an implementation/configuration may
rebase by default. This team's published-branch procedure uses a merge, not force-push.
If --ff-only fails on a long-lived local branch, stop and inspect the divergence with
a lead; do not discard changes with reset --hard just to get unstuck.

## Finish is a merge operation, not a request for approval

The native command exists:

```bash
# NOT the team's protected-branch merge procedure:
# git flow feature finish swerve/field-centric
```

It merges locally and can delete the topic branch; release/hotfix finish can also
merge/tag locally. It does not wait for or substitute for GitHub code-owner review,
required checks or hardware approval. Do not use it to push an unreviewed merge to
`testing` or `main`. Do not give a bot/admin bypass so it can do that.

**Team finalization:** satisfy the PR checks/reviews, then the designated integrator
uses GitHub **Create a merge commit**. This preserves classic Gitflow ancestry.
After GitHub confirms the PR was merged:

```bash
git fetch origin --prune
git switch testing
git pull --ff-only origin testing
git branch -d feature/swerve/field-centric
```

Delete the merged remote feature via GitHub (or have the maintainer do so). If `-d`
refuses, investigate; do not teach unconditional `-D`. Never delete main/testing.

## Release: freeze a candidate without taking unfinished work

```bash
git fetch origin
git switch testing
git pull --ff-only origin testing
git flow release start week-1-event
git flow release publish week-1-event
```

Open `release/week-1-event` → `main`. Only stabilization changes go on this release
branch. New development may continue separately in testing. If main changes, merge
origin/main into the release branch, resolve and retest before seeking new approval.
The current candidate must pass ci-gate, two non-author reviews, code-owner review,
and robot-release-approval. See RELEASE_CHECKLIST.md for the evidence.

Merge via GitHub using a **merge commit**, verify the resulting main tree matches
the validated candidate tree, and make a new annotated tag on that main commit:

```bash
git fetch origin --tags
git switch main
git pull --ff-only origin main
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
# Confirm these against the approved release record before tagging.
git tag -a comp/week-1-v1 -m "Validated week 1 release; see release PR"
git push origin comp/week-1-v1
```

Do not reuse/move tags. Release tags are identifiers, not automatically authenticated
hardware evidence. Restrict tag creation to release personnel where supported.

**Back-merge:** open a same-repository `main` → `testing` PR and merge it with a merge
commit after checks/review. This carries all release fixes back. If conflicts require
work, create `sync/week-1-backmerge` from current testing, merge origin/main into it,
resolve/test, then PR that sync branch → testing. No new feature work in a sync PR.

## Hotfix: repair the released code, not unfinished testing

```bash
git fetch origin
git switch main
git pull --ff-only origin main
git flow hotfix start auto/fix-broken-auto
# Make the smallest fix, add regression coverage and commit.
bash tools/local-check.sh
git flow hotfix publish auto/fix-broken-auto
```

PR `hotfix/auto/fix-broken-auto` → `main`. The same main gates apply; urgency is not
permission to force-push. Validate, merge, tag a new version and back-merge main →
testing. If a release branch is already open, incorporate the hotfix there too and
revalidate before releasing it. Use the last validated version when there is not time
to safely approve a new fix.
