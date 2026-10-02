# Local clone setup

Use this clone at `/Users/anthonycavero/Downloads/FRC_Gitflow_Strict_Starter_Kit`.
The remote is `https://github.com/Antigro09/FRC_Gitflow_Strict_Starter_Kit.git`.
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

The initial real owner and release reviewer is `Antigro09`. Add teammates with the
appropriate access and assign subsystem owners as they join. Two non-author main
approvals are still required, so the current owner cannot approve their own release.
Team number remains `0`; set the real number before any supervised hardware session.
