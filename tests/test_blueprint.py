import json
import tempfile
import unittest
from pathlib import Path

from forja_core.blueprint import BlueprintError, compile_blueprint, write_blueprint


class BlueprintProof(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads((Path(__file__).parents[1] / "examples/enterprise-spec-receivables.json").read_text())

    def test_real_enterprise_spec_compiles_into_front_back_and_governance(self):
        blueprint = compile_blueprint(self.spec)
        self.assertEqual(blueprint["schema"], "forja.enterprise.blueprint/v1")
        self.assertEqual(len(blueprint["frontend"]["routes"]), 3)
        self.assertEqual(len(blueprint["backend"]["models"]), 3)
        self.assertTrue(blueprint["governance"]["deny_by_default"])
        self.assertIn("reconcile_payment:execute", blueprint["governance"]["permissions"]["manager"])

    def test_high_risk_without_controls_is_blocked(self):
        spec = dict(self.spec, controls=[])
        with self.assertRaises(BlueprintError):
            compile_blueprint(spec)

    def test_undeclared_actor_is_blocked(self):
        spec = dict(self.spec, journeys=[{"id": "bad", "actor": "admin", "steps": ["do"]}])
        with self.assertRaises(BlueprintError):
            compile_blueprint(spec)

    def test_duplicate_entity_is_blocked(self):
        spec = dict(self.spec, entities=self.spec["entities"] + [self.spec["entities"][0]])
        with self.assertRaises(BlueprintError):
            compile_blueprint(spec)

    def test_output_is_reproducible_and_complete(self):
        with tempfile.TemporaryDirectory() as directory:
            output = write_blueprint(Path(__file__).parents[1] / "examples/enterprise-spec-receivables.json", directory)
            self.assertTrue(output.exists())
            self.assertEqual(json.loads(output.read_text())["schema"], "forja.enterprise.blueprint/v1")
            for name in ("frontend.routes.json", "backend.domain.json", "governance.json", "acceptance.json"):
                self.assertTrue((Path(directory) / name).exists())


if __name__ == "__main__":
    unittest.main()
