# Import dependencies
import sqlite3
import os


# Define cache function
def cache_keys(pssh: str, keys: str):

    # Connect to database
    dbconnection = sqlite3.connect(f"{os.getcwd()}/databases/key_cache.db")

    # Initialize a cursor
    dbcursor = dbconnection.cursor()

    # Insert PSSH and keys
    dbcursor.execute("INSERT or REPLACE INTO database VALUES (?, ?)", (pssh, keys))

    # Commit the changes
    dbconnection.commit()

    # Close the connection
    dbconnection.close()

def cache_keys_devine(service: str, kid: str, key: str):

    # Connect to database
    dbconnection = sqlite3.connect(f"{os.getcwd()}/databases/devine.db")

    # Initialize a cursor
    dbcursor = dbconnection.cursor()

    # Check if the key already exists
    dbcursor.execute("SELECT COUNT(*) FROM vault WHERE service = ? AND kid = ?", (service, kid))
    row = dbcursor.fetchone()
    if row[0] > 0:
        # Key already exists, perform REPLACE operation
        dbcursor.execute("REPLACE INTO vault VALUES (?, ?, ?)", (service, kid, key))
        operation = "replaced"
    else:
        # Key does not exist, perform INSERT operation
        dbcursor.execute("INSERT INTO vault VALUES (?, ?, ?)", (service, kid, key))
        operation = "inserted"

    # Commit the changes
    dbconnection.commit()

    # Close the connection
    dbconnection.close()

    return operation
