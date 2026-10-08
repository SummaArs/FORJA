import ast
import csv
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).parents[1] / "examples" / "created"


class CreatedExamplesProof(unittest.TestCase):
    def test_local_creation_is_a_discovery_workspace(self):
        project = json.loads((ROOT / "local-acme/forja/project.json").read_text())
        manifest = json.loads((ROOT / "local-acme/forja/manifest.json").read_text())
        self.assertEqual(project["name"], "Acme Local")
        self.assertEqual(project["status"], "discovery")
        self.assertEqual(manifest["portfolio"], "Acme Local")

    def test_ooncore_creation_has_official_shape(self):
        app = json.loads((ROOT / "ooncore-acme/central.app.json").read_text())
        self.assertEqual(app["schemaVersion"], 2)
        self.assertEqual(app["compatibility"]["core"]["minVersion"], "0.6.0")
        for relative in (".ooncore/AGENTS.md", "backend/central.config.js", "frontend/package.json", "oon.deploy.json"):
            self.assertTrue((ROOT / "ooncore-acme" / relative).exists(), relative)

    def test_odoo_creation_has_valid_addon_files(self):
        root = ROOT / "odoo-acme"
        manifest = ast.literal_eval((root / "__manifest__.py").read_text())
        self.assertEqual(manifest["license"], "LGPL-3")
        self.assertTrue(manifest["installable"])
        ast.parse((root / "models/record.py").read_text())
        ET.parse(next((root / "views").glob("*.xml")))
        with (root / "security/ir.model.access.csv").open(newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["perm_create"], "1")


if __name__ == "__main__":
    unittest.main()
