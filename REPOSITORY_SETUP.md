# Administrator activation checklist

The live repository is now BlueCheese1086/GitHub-Etiquette-Repo. The user's explicit
emergency-owner request supersedes the presentation's empty-bypass recommendation.
See [current emergency access](docs/EMERGENCY_OWNER_ACCESS.md); the rest of this
checklist describes ordinary contributor gates and validation.

## 1. Prepare a reviewable baseline

Preserve the actual project. Establish remote main/testing first; integrate the kit
on a setup feature branch. Configure build.gradle, meaningful Java tests, real visible
CODEOWNERS teams with explicit write access, and config/ci-policy.json. Run the checks.
The JSON files under .github/rulesets are templates: files in the repository do not
automatically activate GitHub settings. Avoid conflicting old workflows with the same
job names. Review existing protections instead of deleting them blindly.

Where baseline setup requires initial branch creation, have maintainers coordinate it
before strict rules are active. Limit bypass to the explicitly authorized emergency actors.
Once ready, place the workflow/configuration on the default branch and both protected
lines as appropriate so PR and merge_group events are recognized. Use a sandbox repo
for the negative tests before rolling this into the active robot repository.

## 2. Activate branch rules

Import testing.json and main.json under repository Settings -> Rules -> Rulesets
(or configure equivalent branch protections). Review every field, branch target and
plan capability before activating. The templates require merge commits, no deletions,
no force-push, required PRs, code-owner review, stale-approval dismissal, most-recent
push approval and resolved review threads. testing requires 1 approval, main requires 2.
Preserve these rules for ordinary contributors and add only the documented emergency
actors with `always` bypass. The current allowlist is `Antigro09`, `Blasty25` (Soham),
and `SpaceStudios` (Martin), each an explicit `User` actor on all four repository rulesets.
Do not substitute the organization-owner or administrator
role for an exact-person allowlist. Restrict rule-editing permission itself.
Classic `enforce_admins: false` exempts all repository administrators, so it does
not express a selective owner exception; review existing classic rules separately.

After representative Actions runs have reported the real jobs, select the exact
required check contexts:

| Branch | Required contexts |
| --- | --- |
| testing | ci-gate |
| main | ci-gate, robot-release-approval |

**Bind each required context to the actual GitHub Actions app**, not "any source".
The import templates intentionally omit the app-source binding; set it
from the UI after a genuine run. No fabricated integration ID is supplied. Ensure
job names are unique across every workflow. Inspect a real PR to confirm the merge
box is blocked by the intended checks, rather than relying on a screenshot of YAML.
Keep strict up-to-date requirements enabled. Never use continue-on-error or rely on
a skipped job as a successful required gate.

GitHub's check-name/app-source binding is not a proof that a specific workflow file
has not been changed. CODEOWNERS and review of policy changes remain essential.
Where your organization/Enterprise plan supports required workflows from a centrally
controlled repository, adopt that stronger boundary. This kit does not configure an
organization-wide required workflow or prevent a trusted administrator from editing policy.

## 3. Configure authenticated robot-release review (main only)

Create an environment named **robot-release-review** BEFORE setting the activation
variable. Add the actual release lead/mentor team as required reviewers, enable
**Prevent self-review**, and disallow administrator bypass. Do not add robot access
credentials or secrets; this job never deploys anything. Only one listed environment
reviewer must approve, independently of main's two required PR approvals.

Keep `can_admins_bypass: false`: enabling it would extend environment bypass to all
repository administrators. The selected emergency actors can override the branch's
required release check; that does not approve the environment or prove hardware testing.

For this PR-based approval workflow, allow the relevant PR merge refs. A setting that
allows only the literal main branch can block pull_request runs; GitHub documents
`refs/pull/*/merge` for matching them. Use that selected pattern, or deliberately use
no branch restriction with the main-only workflow, while retaining required reviewers.
Test the actual event/ref behavior on a trial PR.

Once the environment protection is genuinely configured, set the **repository Actions
variable `RELEASE_REVIEW_CONFIGURED` to `true`**. The variable is an administrator's
activation assertion, NOT automatic verification of environment settings. Only admins
should manage it. Without it, the release gate deliberately fails. An automatically
created environment without reviewers would not enforce approval; do not mistake it
for a protected one. Audit this configuration periodically.

The reviewer examines ci-gate and evidence for the **current** candidate commit and
code tree, not merely a PR checkbox. Approve only after the required tests are complete.
A new push/reopen/body edit retriggers this workflow and requires a new review. Wait
for all main checks after incorporating a newly changed base. Do not enable a merge
queue on main in this profile; this approval workflow is PR-only, not merge_group.

**Plan limitations matter:** required environment reviewers are public-repository-only
on GitHub Free/Pro/Team. A private repository needs an eligible Enterprise setup for
this mechanism. If unavailable, keep main blocked until administrators implement an
authenticated equivalent, or explicitly adopt/document a weaker manual-release policy
and change the required checks through review. Never silently mark this gate successful
or set the variable to claim nonexistent protection. Branch/ruleset and queue availability
also depend on repository visibility and plan; verify current GitHub documentation.

## 4. Integration order and optional queue

Baseline: a designated integrator merges one PR at a time with strict up-to-date
checks. After A lands, update B, rerun and reapprove as required. This already prevents
ordinary contributors from merging stale-green candidates. An emergency actor can
override those requirements and must record the exception honestly.

Optional: enable a merge queue for **testing only** where available. Configure the
queue for merge commits and the same ci-gate. The supplied workflow handles merge_group
and does not filter by changed paths. Push events exclude gh-readonly-queue/** to
avoid duplicate/conflicting results on synthetic queue branches; merge_group still
checks the actual queue candidate. Validate a real queue run before requiring it.
GitHub documents merge queues for public organization repositories and private
organization repositories on Enterprise Cloud; confirm availability for your account.
Do not claim a queue prevents all semantic conflicts.

## 5. Competition tags and access

Import competition-tags.json to block changes/deletion of existing comp/** tags.
The selected emergency actors can bypass these restrictions. The immutability
rule does not restrict WHO can create a new tag. Configure a separate
creation ruleset scoped to comp/** with only named release personnel allowed to create
where supported, retaining the same explicit emergency allowlist. Otherwise enforce
release authorization through personnel/access controls and verified release records.
A tag is not proof of hardware approval. Never move a known-good tag.

Only designated personnel should control the competition deployment laptop and robot
network access. The kit's preflight is advisory and does not replace those controls.
Do not use CI to automatically run gradlew deploy. Keep CI on GitHub-hosted isolated
runners, with read-only contents permission and no persistent checkout credentials.
Action commits and Gitleaks binary checksum are pinned; review upgrades separately.
After pulling the official WPILib image, record/pin its verified digest as an additional
supply-chain hardening step. Do not guess the digest.

## 6. Optional local pre-push guard

Check `git config --get core.hooksPath` and inspect existing hooks first. Do not overwrite
another hook setup. With team agreement, enable this kit's hook using:

```bash
chmod +x .githooks/pre-push tools/local-check.sh
git config core.hooksPath .githooks
```

The hook rejects direct main/testing pushes, requires the pushed branch to be checked
out with a clean tree, and runs local checks. It is per-clone and bypassable with
--no-verify. The real enforcement is remote rules. Windows users need Git Bash/Python
for this Bash hook, or can use the supplied PowerShell local-check script manually.
For an authorized emergency direct push, use the explicit per-command override in
[EMERGENCY_OWNER_ACCESS.md](docs/EMERGENCY_OWNER_ACCESS.md); leave the saved hook enabled.

## 7. Prove the protections before declaring success

In a disposable repository/branch, demonstrate each blocked state. Never test by
placing real secrets into a live repo or by moving production tags.

| Trial | Expected result |
| --- | --- |
| Ordinary contributor direct push to testing/main | Rejected by active protection |
| Explicitly allowlisted owner emergency push or own-PR merge | Permitted through bypass; record actual checks and reason |
| Feature PR directly into main or incorrectly named branch | Policy failure |
| Compile error or Java warning | ci-gate fails |
| Formatting violation or PMD violation | ci-gate fails |
| Failing, skipped or zero JUnit tests / absent reports | ci-gate fails |
| Production coverage below either threshold | ci-gate fails |
| Tampered wrapper or a safe synthetic scanner fixture | Validation/scanner fails |
| A prerequisite fails, skips or is cancelled | Final gate does not pass |
| PR B checked before PR A lands | B must revalidate against current integration |
| New commit after approval | Required renewed review; main release approval reruns |
| Ordinary contributor main merge without release approval | Merge remains blocked |
| Unauthorized code-owner/policy edit | Proper owner review required |
| Ordinary contributor updating/deleting an existing comp tag | Rejected by tag rules |

Separately verify reviewers really have access, default branch/ref filters are correct,
all reports are readable, and the release lead can identify the exact deployed revision.
Record who performed these trials and the run/PR links. VALIDATION_REPORT.md describes
local artifact validation only, not completion of this live activation checklist.
