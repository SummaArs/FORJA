import json
import tempfile
import unittest
from pathlib import Path

from forja_core.ai import choose_provider, discover_providers
from forja_core.conversation import conduct


class ConversationProof(unittest.TestCase):
    def test_natural_answers_create_valid_project_without_json_input(self):
        answers = iter([
            "Loja da Ana", "organizar pedidos e clientes", "vendedora e gerente",
            "clientes, pedidos", "criar pedido, acompanhar pedido", "sim", "sim",
        ])
        output = []
        with tempfile.TemporaryDirectory() as root:
            result = conduct(target="local", root=root, input_fn=lambda _: next(answers), output_fn=output.append)
            self.assertTrue(result["ok"])
            spec = json.loads(Path(result["requirements"]).read_text())
            self.assertEqual(spec["name"], "Loja da Ana")
            self.assertTrue(Path(result["blueprint"]).exists())
            self.assertTrue(Path(result["project"]).joinpath("CONVERSA.md").exists())

    def test_cancel_does_not_create_project(self):
        answers = iter(["Projeto", "problema", "equipe", "coisas", "ações", "não", "não"])
        with tempfile.TemporaryDirectory() as root:
            result = conduct(target="local", root=root, input_fn=lambda _: next(answers), output_fn=lambda _: None)
            self.assertFalse(result["ok"])
            self.assertFalse(Path(root, "projeto").exists())

    def test_free_provider_fallback_is_deterministic(self):
        provider = choose_provider(environ={})
        self.assertEqual(provider["id"], "deterministic")
        self.assertTrue(provider["free"])

    def test_provider_discovery_never_claims_uninstalled_tools(self):
        found = discover_providers(environ={})
        self.assertTrue(all("available" in item and item["free"] for item in found))


if __name__ == "__main__":
    unittest.main()
