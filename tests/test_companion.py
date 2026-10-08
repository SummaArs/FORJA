import json
import tempfile
import unittest
from pathlib import Path

from forja_core.companion import build_packet, write_packet


class CompanionProof(unittest.TestCase):
    def test_selective_packet_respects_budget_and_excludes_git_noise(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            (base / "src").mkdir()
            (base / "src/app.py").write_text("def invoices():\n    return True\n")
            (base / "README.md").write_text("invoice application\n")
            (base / ".git").mkdir()
            (base / ".git/secret.txt").write_text("never include")
            packet = build_packet(base, "corrigir invoices", budget=80, limit=10)
            self.assertLessEqual(packet["selection"]["used_chars"], 80)
            self.assertNotIn(".git/secret.txt", packet["selection"]["files"])
            self.assertEqual(len(packet["fingerprint"]), 16)

    def test_write_packet_creates_agent_handoff(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            (base / "README.md").write_text("um projeto")
            out = base / ".forja/companion"
            packet = write_packet(base, "entender o projeto", out, budget=500)
            self.assertTrue((out / "CLAUDE_CONTEXT.md").exists())
            saved = json.loads((out / "context.json").read_text())
            self.assertEqual(saved["fingerprint"], packet["fingerprint"])
            self.assertIn("Regras", (out / "CLAUDE_CONTEXT.md").read_text())

    def test_generated_context_cannot_monopolize_handoff(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            (base / "context.generated.md").write_text("invoice " * 100000)
            (base / "src.py").write_text("def invoice():\n    return True\n")
            (base / "tests.py").write_text("def test_invoice():\n    assert True\n")
            packet = build_packet(base, "corrigir invoice", budget=1200, limit=10)
            self.assertGreaterEqual(packet["selection"]["included"], 2)
            self.assertNotIn("context.generated.md", packet["selection"]["files"])


if __name__ == "__main__":
    unittest.main()
