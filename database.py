import sqlite3
import hashlib
import secrets

DATABASE_NAME = "lost_found.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_type TEXT NOT NULL,
            item_name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            location TEXT,
            date_reported TEXT,
            image_path TEXT,
            contact TEXT,
            status TEXT DEFAULT 'Active'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def create_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    try:
        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, f"{salt}:{password_hash}"))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def verify_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT password
        FROM users
        WHERE username = ?
    """, (username,))

    result = cursor.fetchone()
    connection.close()

    if not result:
        return False

    stored_password = result[0]

    salt, stored_hash = stored_password.split(":")

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    return secrets.compare_digest(password_hash, stored_hash)


def add_report(
    report_type,
    item_name,
    category,
    description,
    location,
    date_reported,
    image_path,
    contact
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO reports (
            report_type,
            item_name,
            category,
            description,
            location,
            date_reported,
            image_path,
            contact
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_type,
        item_name,
        category,
        description,
        location,
        date_reported,
        image_path,
        contact
    ))

    connection.commit()
    connection.close()


def get_reports():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM reports
        ORDER BY id DESC
    """)

    reports = cursor.fetchall()

    connection.close()

    return reports