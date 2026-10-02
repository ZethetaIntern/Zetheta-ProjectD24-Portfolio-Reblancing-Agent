# Local SQLite audit store.

import json
import sqlite3
from datetime import datetime

class AuditStore:
    def __init__(self, path="wealthpilot_audit.db"):
        self.path = path
        with sqlite3.connect(self.path) as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    portfolio_id TEXT,
                    action TEXT,
                    payload TEXT
                )
            """)

    def write(self, portfolio_id, action, payload):
        with sqlite3.connect(self.path) as con:
            con.execute(
                "INSERT INTO audit(timestamp, portfolio_id, action, payload) VALUES (?, ?, ?, ?)",
                (datetime.utcnow().isoformat(), portfolio_id, action, json.dumps(payload, default=str)),
            )
