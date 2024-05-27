import sqlite3
import os
from . import gen_hash


def check_username_exist(username):
    # Connect to the SQLite database
    conn = sqlite3.connect(f'{os.getcwd()}/databases/users.db')
    cursor = conn.cursor()

    # Execute a SELECT query to check if the username exists
    cursor.execute("SELECT * FROM DATABASE WHERE username=?", (username,))

    # Fetch the result
    result = cursor.fetchone()

    # Close the database connection
    conn.close()

    # If result is not None, username exists in the database, return True
    if result:
        return True
    else:
        return False


def check_password(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect(f'{os.getcwd()}/databases/users.db')
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve the password for the given username
    cursor.execute("SELECT hashedpassword FROM DATABASE WHERE username=?", (username,))

    # Fetch the result
    result = cursor.fetchone()

    # Close the database connection
    conn.close()

    # If result is not None, username exists in the database, return the password
    if result[0]:
        if result[0] == gen_hash.generate_md5(username.lower(), password):
            return True
    else:
        return False


def insert_user(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect(f'{os.getcwd()}/databases/users.db')
    cursor = conn.cursor()

    try:
        # Execute an INSERT query to insert the username and password into the users table
        cursor.execute("INSERT INTO DATABASE (username, hashedpassword) VALUES (?, ?)", (username.lower(), gen_hash.generate_md5(username.lower(), password)))
        # Commit the transaction
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        # Rollback the transaction in case of any error
        conn.rollback()
    finally:
        # Close the database connection
        conn.close()
