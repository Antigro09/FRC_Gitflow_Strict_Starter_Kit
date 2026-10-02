# Local clone setup

Use this clone at `/Users/anthonycavero/Downloads/FRC_Gitflow_Strict_Starter_Kit`.
The remote is `https://github.com/BlueCheese1086/GitHub-Etiquette-Repo.git`.
Java 17 is installed in the standard per-user macOS location, and `java -version`
works without a temporary environment override. Git-flow-next 2.1.0 is installed.
Install WPILib VS Code for the integrated robot editor and simulation UI.

Each fresh clone needs its own Gitflow configuration:

```bash
git fetch origin
git flow init --preset=classic --defaults --main=main --develop=testing --feature=feature/ --release=release/ --hotfix=hotfix/
```

Start normal work from current `testing`, then use `git flow feature start` and
`git flow feature publish`; open the PR into `testing`. Keep merge commits and
complete the PR evidence sections. Native `git flow finish` does not perform the
required remote reviews. `main` and `testing` must persist.

Run the complete strict check at the repository root:

```bash
bash tools/local-check.sh
```

This clone uses the optional `.githooks/pre-push` guard. It rejects direct protected
branch pushes and checks the exact committed feature revision. Remote rules remain
the enforcement boundary. Additional clones may enable the same convenience guard:

```bash
chmod +x .githooks/pre-push tools/local-check.sh
git config core.hooksPath .githooks
```

The initial code owner and release reviewer is `Antigro09`. Ordinary contributors
need one non-author testing review or two main reviews. The explicit emergency
allowlist currently contains `Antigro09` and `Blasty25` (Soham), each with
`User`/`always` bypass on all four repository rulesets. Both can merge their own PR
using bypass; GitHub does not allow self-approval. The third intended owner's
identity is pending and has not been granted this exception.
See [emergency owner access](EMERGENCY_OWNER_ACCESS.md) for the per-command direct-push
hook override and the distinction between bypass and release approval. No local
hook automatically grants an owner exception. Add teammates and subsystem owners
with the appropriate access as they join.
Team number remains `0`; set the real number before any supervised hardware session.
