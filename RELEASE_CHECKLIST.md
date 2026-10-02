# Release evidence and deployment checklist

## Candidate evidence (in the PR or an external record)

Record the release/hotfix branch and candidate head SHA, candidate code-tree SHA, and
CI run. Record season/GradleRIO/vendor versions, robot identity and relevant configuration,
test conditions, actual results, tester/reviewer, unresolved risks and a known-good
rollback tag. Use `git rev-parse HEAD` and `git rev-parse 'HEAD^{tree}'` to identify them.
Do not insert a commit's own final SHA into a file inside that same commit.

For changes in scope, test both the subsystem and the integrated robot. Cover safe
startup/disable, command interruption, sensor freshness/dropouts, autonomous selection,
control frame/units, limits, and interactions with other subsystems. Follow the team's
established physical safety procedures; this checklist is not a replacement for them.
Run experiments only in an explicitly authorized practice/bench session, never as an
unreviewed competition deployment. Keep one coordinated operator/session on the robot.

Any relevant code, assets, configuration or base update requires reassessment and
appropriate retesting. Update the PR evidence and obtain renewed reviews. A green build,
coverage number or environmental approval does not prove physical correctness.

## Promotion

Require current ci-gate, two non-author PR approvals, code-owner approval, resolved
threads and the authenticated robot-release-approval. The release lead approves the
current evidence, not an earlier SHA. Merge the main PR using a merge commit. Fetch
main and verify the merged main tree equals the validated candidate tree. If it differs,
stop and validate the actual resulting candidate; do not reuse the earlier sign-off.
Create a new annotated comp/<event>-vN tag on the approved main commit, record the PR,
CI and approval links, and back-merge main -> testing through a PR. Do not move tags.

## Competition station

The deployment lead selects an approved tag from main history and explicitly states
whether this is a new release or an authorized rollback. Use a clean checkout with no
untracked files that could alter the build. Confirm toolchain/vendor/config parity,
fetch main/tags when connectivity permits, verify CI/release approval for the selected
revision and check the recorded tree. Run:

```bash
python3 tools/competition_preflight.py comp/week-1-v1
```

The preflight checks the selected annotated tag, main-branch checkout, clean tree and
origin/main ancestry. It does **not** contact GitHub, authenticate the release record,
compile, inspect the roboRIO, enforce physical access or deploy anything. A stale fetched
origin/main is a limitation. The lead must verify the upstream/evidence separately.
For an approved rollback, prepare the earlier main revision in a dedicated deployment
clone/worktree under lead control; do not reset shared remote main or move its tag.

Only after approval should the authorized deployer build/deploy using the configured
WPILib procedure (for example `./gradlew deploy`) and record the actual deployed tag/SHA,
time, operator and relevant configuration. After deployment, perform the established
post-deploy checks before enabling operation. A main branch name alone cannot tell you
what code is currently on the robot.

If a new patch cannot be safely reviewed/validated in time, use the approved known-good
release. Repair history with a reviewed fix/revert PR, never a force-push reset. Reverting
a merge requires maintainer attention to parent choice and later reintegration.
