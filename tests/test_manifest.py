import json
import tempfile
import unittest
from pathlib import Path

from forja_core import Artifact, validate_manifest


class ManifestProof(unittest.TestCase):
    def test_valid_portfolio(self):
        result = validate_manifest(Path("examples/enterprise-portfolio.json"))
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["artifacts"], 3)

    def test_validated_without_evidence_is_blocked(self):
        raw = {"artifacts": [{"id": "x", "name": "X", "kind": "software", "purpose": "p", "owner": "o", "risk": "low", "state": "validated", "claims": ["c"]}]}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as file:
            json.dump(raw, file)
            file.flush()
            result = validate_manifest(file.name)
        self.assertFalse(result["ok"])
        self.assertTrue(any("evidence" in error for error in result["errors"]))

    def test_high_risk_without_reopening_trigger_is_blocked(self):
        artifact = Artifact("x", "X", "policy", "p", "o", "high", "experiment", ("c",), ("e",), (), ("n",))
        self.assertTrue(any("reopening" in error for error in artifact.validate()))

    def test_duplicate_ids_are_blocked(self):
        raw = {"artifacts": [{"id": "x"}, {"id": "x"}]}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as file:
            json.dump(raw, file)
            file.flush()
            result = validate_manifest(file.name)
        self.assertFalse(result["ok"])
        self.assertIn("unique", result["errors"][0])


if __name__ == "__main__":
    unittest.main()
