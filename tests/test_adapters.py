import tempfile
import unittest
from pathlib import Path

from forja_core.adapters import create_local, create_odoo, create_ooncore, plan


class AdapterProof(unittest.TestCase):
    def test_plan_is_safe_before_apply(self):
        result = plan("ooncore", "/tmp/app", "App")
        self.assertTrue(result["plan_only"])
        self.assertTrue(result["apply_required"])

    def test_local_adapter_creates_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            result = create_local(Path(directory) / "app", "App")
            self.assertTrue(result["ok"])
            self.assertTrue((Path(directory) / "app" / "forja" / "manifest.json").exists())

    def test_odoo_adapter_creates_community_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            result = create_odoo(Path(directory) / "addon", "Gestao Cliente", apply=True)
            self.assertTrue(result["ok"])
            root = Path(directory) / "addon"
            self.assertTrue((root / "__manifest__.py").exists())
            self.assertTrue((root / "models" / "record.py").exists())
            self.assertTrue((root / "security" / "ir.model.access.csv").exists())

    def test_ooncore_without_apply_is_plan_only(self):
        result = create_ooncore("/tmp/app", "App")
        self.assertFalse(result["apply"])
        self.assertTrue(result["read_only"])
        self.assertIn("create-central-oon@0.7.8", result["package"])


if __name__ == "__main__":
    unittest.main()
