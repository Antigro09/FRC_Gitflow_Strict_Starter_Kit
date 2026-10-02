# Emergency owner access

The user's October 2, 2026 instruction adds an emergency exception to the
presentation's original no-bypass policy. The repository is now
[BlueCheese1086/GitHub-Etiquette-Repo](https://github.com/BlueCheese1086/GitHub-Etiquette-Repo).

## Current access

`Antigro09` (GitHub user ID `182770607`) has an explicit `User` bypass with mode
`always` on the four repository rulesets: testing `24368649`, main `24368650`,
competition-tag immutability `24368652`, and tag creation `24368654`.
The other two intended owners' usernames are still required. Their access has not
been configured or inferred from organization membership.

This exception permits direct protected-branch pushes and merging the owner's own
PR without another approval. It can also override required CI/release checks and
the other rules in those rulesets. It is an emergency permission, not evidence
that checks passed, a robot was tested, or deployment was approved. Ordinary
contributors still follow the review and quality requirements in CONTRIBUTING.md.

GitHub does not allow an author to approve their own PR. The permitted action is
to **merge using bypass**, not to create a self-approval. PR #1 was merged into
testing without self-approval after its checks passed:
[PR #1](https://github.com/BlueCheese1086/GitHub-Etiquette-Repo/pull/1), merge commit
`ab0d5c6f9d742f5daf7cbb1410820db8530489f5`.

## Use the exception explicitly

Prefer a PR with recorded purpose, commands/results and the reason for using the
exception. An allowlisted owner can merge an otherwise blocked PR with:

```bash
gh pr merge <PR-number> --repo BlueCheese1086/GitHub-Etiquette-Repo --merge --admin
```

The local pre-push hook deliberately continues to reject direct main/testing
pushes. For an authorized emergency push, inspect and check the exact committed
revision, then bypass that local hook for this one command:

```bash
git -c core.hooksPath=/dev/null push origin HEAD:main
```

Use `HEAD:testing` when testing is the intended destination. This command does not
change the clone's saved hook configuration or grant server permission. GitHub
authenticates the pushing account and applies its configured bypass eligibility.
No hook automatically recognizes owners or silently skips checks.

## Release review and organization scope

The `robot-release-review` environment retains self-review prevention and
`can_admins_bypass: false`. Its approval workflow never deploys. An allowlisted
owner can bypass the branch's required release check without approving that
environment; this must not be reported as hardware sign-off.

The October 2 inventory found 96 organization repositories, these four rulesets,
and five classic branch-protection rules elsewhere with administrator enforcement
disabled. Those classic rules already exempt repository administrators; they do
not restrict the exception to the intended three people. No organization roles or
those other repositories' policies were changed by this repository update.

BlueCheese1086 currently has 14 organization owners, not three. Using the
`OrganizationAdmin` actor would allow all 14; using the repository administrator
role would also include other repository administrators. The current explicit
user entry avoids either expansion. All organization owners retain their existing
power to edit repository settings; an allowlist does not remove that authority.

The organization is on GitHub Free. Repository ruleset bypass is configured per
ruleset; there is no global bypass setting that overrides all other protections.
Organization rulesets covering current and future repositories require Team or
Enterprise. Until then, new repositories and additional protections need a
separate access review. See [ruleset bypass](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
and [organization rulesets](https://docs.github.com/en/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization).
