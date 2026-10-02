#!/usr/bin/env python3
"""Reject empty/skipped/failed tests and missing/low JaCoCo reports, independently of Gradle."""
from __future__ import annotations
import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from ci_policy import PolicyError, validate_config

def parse_xml(path: Path) -> ET.Element:
    raw = path.read_bytes()
    # JaCoCo legitimately emits a DOCTYPE. ElementTree does not load external DTDs;
    # reject entity declarations to avoid internal entity expansion.
    if b"<!ENTITY" in raw.upper():
        raise PolicyError(f"Entity declarations are not allowed in reports: {path}")
    return ET.fromstring(raw)

def verify_tests(paths: list[Path], minimum: int = 1) -> int:
    if not paths:
        raise PolicyError("No JUnit XML reports: tests did not provide evidence.")
    executed = 0
    for path in paths:
        root = parse_xml(path)
        if root.tag not in ("testsuite", "testsuites"):
            raise PolicyError(f"Unexpected JUnit report root in {path}: {root.tag}")
        if root.tag not in ("testsuite", "testsuites"):
            raise PolicyError(f"Unexpected JUnit report root in {path}: {root.tag}")
        cases = list(root.iter("testcase"))
        for suite in root.iter("testsuite"):
            for attr in ("failures", "errors", "skipped", "disabled"):
                if int(suite.get(attr, "0")) != 0:
                    raise PolicyError(f"JUnit {attr} present in {path}")
        for case in cases:
            if any(case.find(tag) is not None for tag in ("failure", "error", "skipped")):
                raise PolicyError(f"Failed or skipped test case in {path}")
        executed += len(cases)
    if executed < minimum:
        raise PolicyError(f"Only {executed} executed tests; minimum is {minimum}.")
    return executed

def verify_coverage(path: Path, line_min: float, branch_min: float) -> dict[str, float]:
    root = parse_xml(path)
    if root.tag != "report":
        raise PolicyError("Expected a JaCoCo <report> root.")
    counters = {c.get("type"): c for c in root.findall("counter")}
    result = {}
    for metric, minimum in (("LINE", line_min), ("BRANCH", branch_min)):
        if metric not in counters:
            raise PolicyError(f"JaCoCo report has no production {metric} counter.")
        c = counters[metric]
        covered, missed = int(c.attrib["covered"]), int(c.attrib["missed"])
        total = covered + missed
        if min(covered, missed) < 0 or total <= 0:
            raise PolicyError(f"JaCoCo {metric} has no measurable production code.")
        ratio = covered / total
        if ratio + 1e-12 < minimum:
            raise PolicyError(f"{metric} coverage {ratio:.2%} < {minimum:.2%}.")
        result[metric] = ratio
    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    a = parser.parse_args()
    try:
        p = json.loads((a.root / "config/ci-policy.json").read_text())
        validate_config(p)
        n = verify_tests(sorted((a.root / "build/test-results/test").glob("TEST-*.xml")), p["minimum_executed_tests"])
        ratios = verify_coverage(a.root / "build/reports/jacoco/test/jacocoTestReport.xml",
                                 p["minimum_line_coverage"], p["minimum_branch_coverage"])
        print(f"Report evidence passed: {n} executed tests, LINE={ratios['LINE']:.2%}, BRANCH={ratios['BRANCH']:.2%}.")
        return 0
    except (PolicyError, OSError, KeyError, ValueError, ET.ParseError) as exc:
        print(f"REPORT FAILURE: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
