# billing_seeder.py

import sqlite3
import os

class BillingSeeder:
    def __init__(self, db_path="billing/billing.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS billing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            status TEXT,
            payment_method TEXT,
            created_at TEXT,
            paid_at TEXT,
            note TEXT
        )
        """)
        self.conn.commit()

    def seed_data(self):
        billing_records = [
            (1, 100.0, 'paid', 'credit_card', '2025-06-01', '2025-06-02', 'June bill'),
            (1, 250.0, 'pending', 'paypal', '2025-07-01', None, 'July bill'),
            (2, 150.0, 'paid', 'bank_transfer', '2025-06-15', '2025-06-16', 'Mid-June bill'),
        ]

        for record in billing_records:
            self.cursor.execute("""
                INSERT INTO billing (user_id, amount, status, payment_method, created_at, paid_at, note)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, record)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def run(self):
        self.create_table()

        # Check if data already exists
        self.cursor.execute("SELECT COUNT(*) FROM billing")
        count = self.cursor.fetchone()[0]

        if count == 0:
            print("Seeding billing database...")
            self.seed_data()
        else:
            print("Billing table already has data, skipping seeding.")
