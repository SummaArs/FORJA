import json
import tempfile
import unittest
from pathlib import Path
from forja_core.executor import ExecutionPolicy, execute, execution_plan


class ExecutorProof(unittest.TestCase):
    def setUp(self):
        self.spec=json.loads((Path(__file__).parents[1]/'examples/enterprise-spec-receivables.json').read_text())

    def test_plan_never_writes(self):
        with tempfile.TemporaryDirectory() as d:
            result=execute(self.spec, Path(d)/'app')
            self.assertEqual(result['mode'], 'plan-only')
            self.assertFalse((Path(d)/'app').exists())

    def test_apply_creates_front_backend_and_passes_checks(self):
        with tempfile.TemporaryDirectory() as d:
            result=execute(self.spec, Path(d)/'app', ExecutionPolicy(apply=True))
            root=Path(d)/'app'
            self.assertTrue(result['ok'])
            self.assertTrue((root/'frontend/index.html').exists())
            self.assertTrue((root/'backend/app.py').exists())
            self.assertTrue(result['checks']['tests'])

    def test_invalid_blueprint_is_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                execute(dict(self.spec, controls=[]), Path(d)/'app', ExecutionPolicy(apply=True))


if __name__=='__main__': unittest.main()
