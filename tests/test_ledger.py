import tempfile
import unittest
from pathlib import Path

from forja_ledger import Entry, Ledger, LedgerError


class LedgerProof(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = Ledger(Path(self.tmp.name) / "ledger.sqlite")

    def tearDown(self):
        self.ledger.close()
        self.tmp.cleanup()

    def test_valid_entry(self):
        entry = Entry("A-1", "consultoria", 1000)
        self.assertEqual(self.ledger.record(entry), "recorded")
        self.assertEqual(self.ledger.get("A-1"), entry)

    def test_negative_amount_changes_nothing(self):
        with self.assertRaises(LedgerError):
            self.ledger.record(Entry("A-2", "invalid", -1))
        self.assertEqual(self.ledger.count(), 0)

    def test_unknown_currency_changes_nothing(self):
        with self.assertRaises(LedgerError):
            self.ledger.record(Entry("A-3", "invalid", 100, "USD"))
        self.assertEqual(self.ledger.count(), 0)

    def test_idempotent_replay_does_not_duplicate(self):
        entry = Entry("A-4", "same intention", 500)
        self.assertEqual(self.ledger.record(entry), "recorded")
        self.assertEqual(self.ledger.record(entry), "replayed")
        self.assertEqual(self.ledger.count(), 1)
        self.assertEqual(len(self.ledger.audit_for("A-4")), 1)

    def test_reusing_key_with_changed_payload_is_rejected(self):
        self.ledger.record(Entry("A-5", "original", 500))
        with self.assertRaises(LedgerError):
            self.ledger.record(Entry("A-5", "changed", 501))
        self.assertEqual(self.ledger.get("A-5"), Entry("A-5", "original", 500))

    def test_crash_before_commit_does_not_persist(self):
        with self.assertRaises(RuntimeError):
            self.ledger.record(Entry("A-6", "before", 600), crash_at="before_commit")
        self.assertEqual(self.ledger.count(), 0)

    def test_crash_after_commit_is_safe_to_replay(self):
        entry = Entry("A-7", "after", 700)
        with self.assertRaises(RuntimeError):
            self.ledger.record(entry, crash_at="after_commit")
        self.assertEqual(self.ledger.count(), 1)
        self.assertEqual(self.ledger.record(entry), "replayed")

    def test_audit_trail_exists(self):
        self.ledger.record(Entry("A-8", "audited", 800))
        audit = self.ledger.audit_for("A-8")
        self.assertEqual(audit[0]["action"], "recorded")

    def test_reconciliation_detects_missing_and_mismatch(self):
        self.ledger.record(Entry("A-9", "local", 900))
        result = self.ledger.reconcile([Entry("A-9", "changed", 900), Entry("A-10", "missing", 1000)])
        self.assertFalse(result["ok"])
        self.assertEqual(result["missing"], ["A-10"])
        self.assertEqual(result["mismatched"], ["A-9"])

    def test_reconciliation_passes_for_same_source(self):
        entries = [Entry("A-11", "one", 1100), Entry("A-12", "two", 1200)]
        for entry in entries:
            self.ledger.record(entry)
        self.assertEqual(self.ledger.reconcile(entries), {"ok": True, "missing": [], "unexpected": [], "mismatched": [], "source_count": 2, "stored_count": 2})


if __name__ == "__main__":
    unittest.main()
