#!/usr/bin/env python3
"""Advisory local release identity guard. Does not deploy or verify remote approval."""
from __future__ import annotations
import argparse
import re
import subprocess
import sys

def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, stderr=subprocess.STDOUT).strip()

def validate_tag_name(tag: str) -> bool:
    return bool(re.fullmatch(r"comp/[a-z0-9]+(?:-[a-z0-9]+)*", tag))

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("approved_tag")
    a = p.parse_args()
    try:
        if not validate_tag_name(a.approved_tag):
            raise ValueError("Use a comp/<event>-vN lowercase kebab-case tag.")
        if git("branch", "--show-current") != "main":
            raise ValueError("Competition checkout must be on local main under lead control.")
        if git("status", "--porcelain", "--untracked-files=all"):
            raise ValueError("Working tree must be clean, including untracked files.")
        ref = "refs/tags/" + a.approved_tag
        if git("cat-file", "-t", ref) != "tag":
            raise ValueError("Expected an annotated release tag.")
        head, target = git("rev-parse", "HEAD"), git("rev-parse", ref + "^{commit}")
        if head != target:
            raise ValueError("Current checkout does not match the selected approved tag.")
        subprocess.run(["git", "merge-base", "--is-ancestor", head, "refs/remotes/origin/main"], check=True)
        print(f"Local identity checks passed: {a.approved_tag}\nCommit: {head}\nTree: {git('rev-parse', 'HEAD^{tree}')}")
        print("STOP: lead must still verify fresh upstream state, matching CI/test evidence, toolchain/config and approval. Nothing was deployed.")
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"PREFLIGHT FAILURE: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
