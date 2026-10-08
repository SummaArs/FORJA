import json
import tempfile
import unittest
from pathlib import Path

from forja_core import connect_repository, init_workspace, inspect_repository


class WorkspaceProof(unittest.TestCase):
    def test_init_is_didactic_and_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            location = init_workspace(directory, "cliente-x", "Gustavo")
            second = init_workspace(directory, "cliente-x", "Gustavo")
            self.assertEqual(location, second)
            self.assertTrue((location / "manifest.json").exists())

    def test_local_connection_is_read_only_discovery(self):
        with tempfile.TemporaryDirectory() as workspace, tempfile.TemporaryDirectory() as repo:
            repo_path = Path(repo)
            (repo_path / ".git").mkdir()
            (repo_path / "README.md").write_text("OonCore")
            record = connect_repository(workspace, repo_path, "ooncore")
            self.assertTrue(record["read_only"])
            self.assertTrue(record["safe_to_connect"])
            saved = json.loads((Path(workspace) / "forja" / "connection-ooncore.json").read_text())
            self.assertEqual(saved["mode"], "local-read-only")
            self.assertEqual((repo_path / "README.md").read_text(), "OonCore")

    def test_remote_reference_does_not_clone_or_execute(self):
        result = inspect_repository("https://github.com/example/ooncore.git", "ooncore")
        self.assertEqual(result["mode"], "remote-reference")
        self.assertTrue(result["safe_to_connect"])


if __name__ == "__main__":
    unittest.main()
