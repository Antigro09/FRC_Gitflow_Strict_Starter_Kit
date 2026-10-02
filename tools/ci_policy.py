#!/usr/bin/env python3
"""Fail-closed repository/PR checks. Python 3.10+, standard library only."""
from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
TITLE = re.compile(r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert|release|sync)(\([a-z0-9-]+\))?!?: \S.+$")
HEADINGS = ("Issue and purpose", "Changes and shared interfaces", "Test evidence", "Robot validation", "Risk and rollback")
REQUIRED = (
    "CONTRIBUTING.md", ".github/CODEOWNERS", ".github/pull_request_template.md",
    ".github/workflows/robot-ci.yml", ".github/workflows/release-review.yml",
    "config/ci-policy.json", "config/pmd/ruleset.xml", "gradle/quality.gradle",
    "build.gradle", "gradlew", "gradlew.bat", "gradle/wrapper/gradle-wrapper.jar",
    "gradle/wrapper/gradle-wrapper.properties", "tools/verify_reports.py",
)

class PolicyError(ValueError):
    """A policy failure that should block a merge."""

def validate_config(p: dict) -> None:
    if p.get("schema_version") != 1 or p.get("configured") is not True:
        raise PolicyError("CI kit is not configured; complete docs/BUILD_INTEGRATION.md.")
    if p.get("language") != "java":
        raise PolicyError("This profile requires a single-project Java robot.")
    if p.get("integration_branch") != "testing" or p.get("release_branch") != "main":
        raise PolicyError("This workflow/rules profile uses testing and main; update all files together.")
    names = p.get("subsystems")
    if not isinstance(names, list) or not names or any(not isinstance(x, str) or not re.fullmatch(SLUG, x) for x in names):
        raise PolicyError("subsystems must be a nonempty list of lowercase kebab-case names.")
    for key in ("minimum_line_coverage", "minimum_branch_coverage"):
        v = p.get(key)
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 < v <= 1:
            raise PolicyError(f"Invalid coverage policy: {key}")
    if type(p.get("minimum_executed_tests")) is not int or p["minimum_executed_tests"] < 1:
        raise PolicyError("At least one executed test must be required.")
    if p.get("allow_skipped_tests") is not False:
        raise PolicyError("The strict profile does not allow skipped tests.")

def kind(branch: str, p: dict) -> str:
    if branch in ("main", "testing"):
        return branch
    subsystem = "(?:" + "|".join(re.escape(s) for s in p["subsystems"]) + ")"
    for prefix, body in (("feature", subsystem + "/" + SLUG), ("hotfix", subsystem + "/" + SLUG), ("release", SLUG), ("sync", SLUG)):
        if re.fullmatch(prefix + "/" + body, branch):
            return prefix
    raise PolicyError(f"Invalid branch name: {branch!r}; read CONTRIBUTING.md.")

def validate_route(base: str, head: str, same_repository: bool, p: dict) -> None:
    k = kind(head, p)
    if base == "testing" and k == "feature":
        return
    if base == "testing" and k in ("main", "sync") and same_repository:
        return
    if base == "main" and k in ("release", "hotfix") and same_repository:
        return
    raise PolicyError(f"Disallowed PR route: {head} -> {base}. Releases/hotfixes/sync must be same-repository.")

def validate_body(body: str) -> None:
    if "REPLACE_ME" in body:
        raise PolicyError("Replace all PR template placeholders with actual evidence.")
    for heading in HEADINGS:
        match = re.search(r"(?m)^## " + re.escape(heading) + r"\s*\n([\s\S]*?)(?=^## |\Z)", body)
        if not match or len(match.group(1).strip()) < 15:
            raise PolicyError(f"PR section is missing or too short: {heading}")

def validate_event(event_name: str, event: dict, p: dict, ref_name: str = "") -> None:
    if event_name == "pull_request":
        pr = event["pull_request"]
        validate_route(pr["base"]["ref"], pr["head"]["ref"],
                       pr["base"]["repo"]["full_name"] == (pr["head"].get("repo") or {}).get("full_name"), p)
        if pr.get("draft", False):
            raise PolicyError("Draft PR: publish normally, mark ready only when reviewable.")
        if not TITLE.fullmatch(pr.get("title", "")):
            raise PolicyError("Use a meaningful type(scope): description PR title.")
        validate_body(pr.get("body") or "")
    elif event_name == "push":
        kind(ref_name, p)
    elif event_name == "merge_group":
        if event.get("merge_group", {}).get("base_ref") != "refs/heads/testing":
            raise PolicyError("This profile supports merge queues on testing only.")
    elif event_name != "local":
        raise PolicyError(f"Unsupported event: {event_name}")

def check_files(root: Path) -> None:
    missing = [f for f in REQUIRED if not (root / f).is_file()]
    if missing:
        raise PolicyError("Missing required project/kit files: " + ", ".join(missing))
    owners = (root / ".github/CODEOWNERS").read_text()
    active = "\n".join(line for line in owners.splitlines() if line.strip() and not line.lstrip().startswith("#"))
    if "@YOUR-ORG" in active or not re.search(r"(?m)^\*\s+@\S+", active):
        raise PolicyError("Configure real CODEOWNERS with a catch-all owner; placeholder teams are invalid.")
    build = (root / "build.gradle").read_text()
    if "com.diffplug.spotless" not in build or not re.search(r"apply\s+from:\s*['\"]gradle/quality\.gradle['\"]", build):
        raise PolicyError("Root build.gradle must integrate Spotless and gradle/quality.gradle.")
    # JSON assets and vendor dependencies must parse. Schema/physical behavior need separate tests.
    for folder in ("vendordeps", "src/main/deploy"):
        for f in (root / folder).rglob("*.json"):
            try:
                json.loads(f.read_text())
            except (ValueError, UnicodeError) as exc:
                raise PolicyError(f"Invalid JSON asset: {f.relative_to(root)}: {exc}") from exc

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        p = json.loads((args.root / "config/ci-policy.json").read_text())
        validate_config(p)
        check_files(args.root)
        if args.local:
            branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=args.root, text=True).strip()
            kind(branch, p)
        else:
            event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
            validate_event(os.environ["GITHUB_EVENT_NAME"], event, p, os.environ.get("GITHUB_REF_NAME", ""))
        print("Repository policy passed.")
        return 0
    except (PolicyError, OSError, KeyError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"POLICY FAILURE: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
