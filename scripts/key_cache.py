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
