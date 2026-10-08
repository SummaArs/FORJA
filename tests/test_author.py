import tempfile
import unittest
from pathlib import Path

from forja_core.author import create_author_kit


class AuthorProof(unittest.TestCase):
    def test_author_kit_creates_learning_path_without_product_code(self):
        answers = {
            "name": "Agenda da Oficina",
            "problem": "organizar serviços",
            "users": "mecânico",
            "things": "clientes e serviços",
            "first_feature": "cadastrar cliente",
            "risk": "não",
            "target": "local",
        }
        with tempfile.TemporaryDirectory() as root:
            result = create_author_kit(answers, root)
            project = Path(result["project"])
            self.assertTrue((project / "NEXT_STEP.md").exists())
            self.assertTrue((project / "BUILD_LOG.md").exists())
            self.assertTrue((project / "blueprint" / "blueprint.json").exists())
            self.assertFalse((project / "app.py").exists())
            self.assertIn("cadastrar cliente", (project / "NEXT_STEP.md").read_text())


if __name__ == "__main__":
    unittest.main()
