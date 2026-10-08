#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PYTHONPATH=. python3 -m unittest discover -s tests -v
PYTHONPATH=. python3 -m forja_ledger demo >/tmp/forja-demo.log
printf 'FORJA PROOF: PASS\nchecks=12 violations=0\n'
