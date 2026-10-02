#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python3 tools/ci_policy.py --local
python3 -m unittest discover -s tools/tests -v
git diff --check
git diff --cached --check
chmod +x gradlew
./gradlew --no-daemon --stacktrace clean ciVerify
python3 tools/verify_reports.py
printf '\nLocal checks passed. Server wrapper validation, secret scan and reviews still apply.\n'
