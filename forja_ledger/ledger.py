from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


class LedgerError(ValueError):
    """Business input rejected without changing state."""


@dataclass(frozen=True)
class Entry:
    key: str
    description: str
    amount_cents: int
    currency: str = "BRL"
    status: str = "recorded"


class Ledger:
    """A small SQLite ledger with explicit source identity and audit history."""

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.path = str(path)
        self.db = sqlite3.connect(self.path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.execute("PRAGMA journal_mode = WAL")
        self._schema()

    def close(self) -> None:
        self.db.close()

    def _schema(self) -> None:
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS entries (
                key TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
                currency TEXT NOT NULL CHECK(currency = 'BRL'),
                status TEXT NOT NULL CHECK(status = 'recorded'),
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_key TEXT NOT NULL,
                action TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        self.db.commit()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _validate(entry: Entry) -> None:
        if not entry.key or len(entry.key) > 120:
            raise LedgerError("key must be non-empty and at most 120 characters")
        if not entry.description.strip():
            raise LedgerError("description is required")
        if entry.amount_cents <= 0:
            raise LedgerError("amount_cents must be positive")
        if entry.currency != "BRL":
            raise LedgerError("only BRL is supported in this example")
        if entry.status != "recorded":
            raise LedgerError("unknown status")

    def record(self, entry: Entry, crash_at: str | None = None) -> str:
        """Record once. Replay returns 'replayed'; invalid input changes nothing.

        crash_at='before_commit' or 'after_commit' exists only for adversarial tests.
        """
        self._validate(entry)
        payload = json.dumps(entry.__dict__, sort_keys=True, separators=(",", ":"))
        existing = self.db.execute("SELECT payload_json FROM entries WHERE key = ?", (entry.key,)).fetchone()
        if existing:
            if existing["payload_json"] != payload:
                raise LedgerError("idempotency key reused with a different payload")
            return "replayed"

        now = self._now()
        try:
            self.db.execute("BEGIN IMMEDIATE")
            self.db.execute(
                "INSERT INTO entries(key, description, amount_cents, currency, status, payload_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (entry.key, entry.description, entry.amount_cents, entry.currency, entry.status, payload, now),
            )
            self.db.execute(
                "INSERT INTO audit(event_key, action, payload_json, created_at) VALUES (?, ?, ?, ?)",
                (entry.key, "recorded", payload, now),
            )
            if crash_at == "before_commit":
                raise RuntimeError("simulated crash before commit")
            self.db.commit()
        except Exception:
            self.db.rollback()
            if crash_at == "before_commit":
                raise
            raise
        if crash_at == "after_commit":
            raise RuntimeError("simulated process death after commit")
        return "recorded"

    def get(self, key: str) -> Entry | None:
        row = self.db.execute("SELECT key, description, amount_cents, currency, status FROM entries WHERE key = ?", (key,)).fetchone()
        return Entry(**dict(row)) if row else None

    def audit_for(self, key: str) -> list[dict]:
        return [dict(row) for row in self.db.execute("SELECT * FROM audit WHERE event_key = ? ORDER BY id", (key,))]

    def reconcile(self, source: Iterable[Entry]) -> dict:
        source_map = {entry.key: entry for entry in source}
        stored_rows = self.db.execute("SELECT key, description, amount_cents, currency, status FROM entries").fetchall()
        stored_map = {row["key"]: Entry(**dict(row)) for row in stored_rows}
        missing = sorted(set(source_map) - set(stored_map))
        unexpected = sorted(set(stored_map) - set(source_map))
        mismatched = sorted(key for key in set(source_map) & set(stored_map) if source_map[key] != stored_map[key])
        return {"ok": not (missing or unexpected or mismatched), "missing": missing, "unexpected": unexpected, "mismatched": mismatched, "source_count": len(source_map), "stored_count": len(stored_map)}

    def count(self) -> int:
        return int(self.db.execute("SELECT COUNT(*) FROM entries").fetchone()[0])
