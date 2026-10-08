from __future__ import annotations

import argparse
import json
from pathlib import Path

from .manifest import validate_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="FORJA Enterprise OS")
    parser.add_argument("command", choices=["check"])
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    result = validate_manifest(args.manifest)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["ok"]:
        raise SystemExit(1)
    print(f"FORJA MANIFEST: PASS ({result['artifacts']} artifacts)")


if __name__ == "__main__":
    main()
