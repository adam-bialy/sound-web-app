import sqlite3


def create_table():
    connection = sqlite3.connect("sound-users.db")
    connection.execute("""
        CREATE TABLE "Users" (
        "user_id"	INTEGER,
        "low"	INTEGER NOT NULL,
        "high"	INTEGER NOT NULL,
        "range"	INTEGER NOT NULL,
        PRIMARY KEY("user_id" AUTOINCREMENT)
        );
        """)
    connection.commit()
    connection.close()


def insert_record(low, high, hrange):
    connection = sqlite3.connect("sound-users.db")
    connection.execute("""
        INSERT INTO Users (low, high, range) VALUES
        (?, ?, ?)
    """, (low, high, hrange))
    connection.commit()
    connection.close()


def select_all():
    connection = sqlite3.connect("sound-users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users")
    result = cursor.fetchall()
    connection.close()
    return result


def select_specific_columns(*columns):
    connection = sqlite3.connect("sound-users.db")
    cursor = connection.cursor()
    string = f"SELECT {', '.join(columns)} FROM Users"
    cursor.execute(string)
    result = cursor.fetchall()
    connection.close()
    return result
