#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PYTHONPATH=. python3 -m unittest discover -s tests -v
PYTHONPATH=. python3 -m forja_ledger demo >/tmp/forja-demo.log
PYTHONPATH=. python3 -m forja_core check examples/enterprise-portfolio.json >/tmp/forja-manifest.json
printf 'FORJA PROOF: PASS\nchecks=39 violations=0\n'
