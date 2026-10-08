from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from .ledger import Entry, Ledger


def demo() -> None:
    with tempfile.TemporaryDirectory() as directory:
        ledger = Ledger(Path(directory) / "demo.sqlite")
        source = [
            Entry("INV-001", "servidor local", 1990),
            Entry("INV-002", "domínio", 4990),
        ]
        for entry in source:
            print(entry.key, ledger.record(entry))
        print(source[0].key, ledger.record(source[0]))
        print("reconciliation=", ledger.reconcile(source))
        print("audit_entries=", len(ledger.audit_for("INV-001")))
        ledger.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Forja Ledger — demo local sem custo")
    parser.add_argument("command", choices=["demo"])
    args = parser.parse_args()
    if args.command == "demo":
        demo()


if __name__ == "__main__":
    main()
