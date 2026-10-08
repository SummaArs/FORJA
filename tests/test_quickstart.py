import json
import tempfile
import unittest
from pathlib import Path

from forja_core.quickstart import create_quickstart


class QuickstartProof(unittest.TestCase):
    def test_one_simple_command_creates_a_valid_project(self):
        with tempfile.TemporaryDirectory() as directory:
            result = create_quickstart("Minha Loja", directory, target="ooncore")
            root = Path(result["project"])
            spec = json.loads((root / "requirements.json").read_text())
            blueprint = json.loads((root / "blueprint/blueprint.json").read_text())
            self.assertEqual(spec["target"], "ooncore")
            self.assertEqual(blueprint["schema"], "forja.enterprise.blueprint/v1")
            self.assertTrue((root / "README.md").exists())

    def test_name_becomes_safe_directory_name(self):
        with tempfile.TemporaryDirectory() as directory:
            result = create_quickstart("Loja São José!", directory)
            self.assertTrue(result["project"].endswith("loja-s-o-jos"))


if __name__ == "__main__":
    unittest.main()
