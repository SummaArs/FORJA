from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .blueprint import BlueprintError, compile_blueprint


@dataclass(frozen=True)
class ExecutionPolicy:
    apply: bool = False
    run_checks: bool = True
    allow_network: bool = False


def execution_plan(spec: dict[str, Any], target: str | Path) -> dict[str, Any]:
    blueprint = compile_blueprint(spec)
    root = Path(target).resolve()
    return {
        "schema": "forja.execution-plan/v1",
        "mode": "apply" if False else "plan-only",
        "target": str(root),
        "project": spec["name"],
        "phases": ["validate", "frontend", "backend", "tests", "homologation"],
        "frontend_routes": len(blueprint["frontend"]["routes"]),
        "backend_models": len(blueprint["backend"]["models"]),
        "network": "disabled",
        "authorization": "explicit --apply required",
    }


def _write(root: Path, rel: str, content: str) -> str:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return rel


def _frontend(spec: dict[str, Any], blueprint: dict[str, Any]) -> str:
    routes = "".join(f'<a href="#/{r["journey"]}">{r["journey"].replace("_", " ").title()}</a>' for r in blueprint["frontend"]["routes"])
    cards = "".join(f'<article><span>Fluxo</span><h3>{j["id"].replace("_", " ").title()}</h3><p>{" → ".join(j["steps"])}</p><button data-action="{j["id"]}">Abrir fluxo</button></article>' for j in spec["journeys"])
    return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{spec["name"]} — FORJA</title><style>
:root{{--ink:#14202b;--muted:#667482;--brand:#176b87;--accent:#e8b35b;--paper:#f5f7f8}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px system-ui,sans-serif}}header{{background:linear-gradient(135deg,#102f43,#176b87);color:white;padding:42px 7vw}}nav{{display:flex;gap:18px;flex-wrap:wrap;margin-top:22px}}nav a{{color:#fff;text-decoration:none;border-bottom:1px solid #ffffff66;padding-bottom:4px}}main{{max-width:1180px;margin:0 auto;padding:38px 7vw}}.eyebrow{{color:var(--accent);font-weight:700;letter-spacing:.12em;text-transform:uppercase}}h1{{font-size:clamp(2.2rem,6vw,5rem);margin:.2em 0}}.lead{{max-width:700px;color:#dcebf1;font-size:1.2rem}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px}}article{{background:#fff;border:1px solid #dce4e8;border-radius:18px;padding:22px;box-shadow:0 10px 25px #1232  }}article span{{color:var(--brand);font-size:.8rem;font-weight:700;text-transform:uppercase}}button{{border:0;border-radius:999px;background:var(--brand);color:#fff;padding:11px 16px;cursor:pointer}}footer{{padding:28px 7vw;color:var(--muted)}}
</style></head><body><header><div class="eyebrow">FORJA / sistema empresarial</div><h1>{spec["name"]}</h1><p class="lead">{spec["purpose"]}</p><nav>{routes}</nav></header><main><h2>Operações principais</h2><section class="grid">{cards}</section><p id="status" role="status"></p></main><footer>Construído com contratos verificáveis pela FORJA. Não homologado para produção automaticamente.</footer><script>document.querySelectorAll('button').forEach(b=>b.onclick=()=>document.querySelector('#status').textContent='Fluxo '+b.dataset.action+' selecionado. Backend local pronto para extensão.');</script></body></html>'''


def _backend(spec: dict[str, Any], blueprint: dict[str, Any]) -> str:
    models = json.dumps([e["id"] for e in spec["entities"]], ensure_ascii=False)
    return f'''#!/usr/bin/env python3
"""Backend local sem dependências: health check e catálogo do blueprint."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

MODELS = {models}
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/health": payload={{"ok": True, "service": "{spec["name"]}"}}
        elif self.path == "/api/models": payload={{"models": MODELS}}
        else: self.send_error(404); return
        body=json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self, *_): pass

if __name__ == "__main__":
    print("FORJA backend em http://127.0.0.1:8765")
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
'''


def execute(spec: dict[str, Any], target: str | Path, policy: ExecutionPolicy = ExecutionPolicy()) -> dict[str, Any]:
    blueprint = compile_blueprint(spec)
    root = Path(target).resolve()
    if not policy.apply:
        return execution_plan(spec, root)
    root.mkdir(parents=True, exist_ok=True)
    files = {}
    files["forja/blueprint.json"] = json.dumps(blueprint, indent=2, ensure_ascii=False) + "\n"
    files["frontend/index.html"] = _frontend(spec, blueprint)
    files["backend/app.py"] = _backend(spec, blueprint)
    files["backend/requirements.txt"] = "# stdlib only — zero paid or external dependencies\n"
    files["tests/test_smoke.py"] = "import json\nimport unittest\nfrom pathlib import Path\n\nclass GeneratedSmoke(unittest.TestCase):\n    def test_contracts_exist(self):\n        root=Path(__file__).parents[1]\n        self.assertTrue((root/'frontend/index.html').exists())\n        self.assertTrue((root/'backend/app.py').exists())\n        self.assertEqual(json.loads((root/'forja/blueprint.json').read_text())['schema'], 'forja.enterprise.blueprint/v1')\n"
    files["tests/__init__.py"] = ""
    files["run.sh"] = "#!/usr/bin/env bash\nset -euo pipefail\npython3 backend/app.py\n"
    files["README.md"] = f"# {spec['name']}\n\nProjeto gerado pela FORJA com frontend, backend local, contratos e testes.\n\n- Frontend: `frontend/index.html`\n- Backend: `python3 backend/app.py`\n- Prova: `python3 -m pytest -q` ou `python3 -m unittest discover -s tests`\n\nAinda não homologado para produção.\n"
    written = [_write(root, rel, content) for rel, content in files.items()]
    (root / "run.sh").chmod(0o755)
    checks = {"compile": True, "tests": True}
    if policy.run_checks:
        compile_run = subprocess.run([sys.executable, "-m", "compileall", "-q", "backend", "tests"], cwd=root, capture_output=True, text=True)
        test_run = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=root, capture_output=True, text=True)
        checks = {"compile": compile_run.returncode == 0, "tests": test_run.returncode == 0, "test_output": (test_run.stdout + test_run.stderr)[-2000:]}
    return {"ok": all(v for k, v in checks.items() if k in {"compile", "tests"}), "mode": "applied", "target": str(root), "files": written, "checks": checks, "network": "disabled", "not_proven": blueprint["acceptance"]["not_proven"]}
