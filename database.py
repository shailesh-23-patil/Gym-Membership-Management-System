import sqlite3
from pathlib import Path
from datetime import date, timedelta

DB_PATH = Path(__file__).parent / "gym.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Admin', 'Staff'))
        );

        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            gender TEXT,
            address TEXT,
            joined_on TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active'
        );

        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            duration_days INTEGER NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            active INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS memberships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL REFERENCES members(id),
            plan_id INTEGER NOT NULL REFERENCES plans(id),
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active'
        );

        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            membership_id INTEGER NOT NULL
                REFERENCES memberships(id),
            amount REAL NOT NULL,
            payment_date TEXT NOT NULL,
            method TEXT NOT NULL,
            note TEXT
        );
        """)

        if conn.execute("SELECT COUNT(*) FROM plans").fetchone()[0] == 0:
            conn.executemany(
                """INSERT INTO plans
                (name, duration_days, price, description)
                VALUES (?, ?, ?, ?)""",
                [
                    ("Monthly", 30, 1200, "30-day membership"),
                    ("Quarterly", 90, 3200, "90-day membership"),
                    ("Half-Yearly", 180, 6000, "180-day membership"),
                    ("Annual", 365, 10000, "365-day membership"),
                ],
            )

        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            from auth import hash_password

            salt, password_hash = hash_password("Admin@123")

            conn.execute(
                """INSERT INTO users
                (username, password_hash, salt, role)
                VALUES (?, ?, ?, ?)""",
                ("admin", password_hash, salt, "Admin"),
            )


def query_df(sql, params=()):
    import pandas as pd

    with get_connection() as conn:
        return pd.read_sql_query(sql, conn, params=params)


def execute(sql, params=()):
    with get_connection() as conn:
        cursor = conn.execute(sql, params)
        return cursor.lastrowid


def get_one(sql, params=()):
    with get_connection() as conn:
        return conn.execute(sql, params).fetchone()


def add_membership(
    member_id, plan_id, start_date, amount, method, note=""
):
    plan = get_one(
        "SELECT duration_days FROM plans WHERE id = ?",
        (plan_id,),
    )

    if plan is None:
        raise ValueError("Membership plan not found.")

    start = date.fromisoformat(start_date)
    end = start + timedelta(days=int(plan["duration_days"]))

    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO memberships
            (member_id, plan_id, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?)""",
            (
                member_id,
                plan_id,
                start.isoformat(),
                end.isoformat(),
                "Active",
            ),
        )

        membership_id = cursor.lastrowid

        conn.execute(
            """INSERT INTO payments
            (membership_id, amount, payment_date, method, note)
            VALUES (?, ?, ?, ?, ?)""",
            (
                membership_id,
                float(amount),
                date.today().isoformat(),
                method,
                note,
            ),
        )

        conn.execute(
            "UPDATE members SET status = 'Active' WHERE id = ?",
            (member_id,),
        )

    return end.isoformat()


def refresh_membership_statuses():
    today = date.today().isoformat()

    with get_connection() as conn:
        conn.execute(
            """UPDATE memberships
            SET status = 'Expired'
            WHERE end_date < ? AND status = 'Active'""",
            (today,),
        )