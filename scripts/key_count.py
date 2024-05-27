# Import dependencies
import sqlite3
import os


# Define cache function
def count_keys():

    # Connect to database
    dbconnection = sqlite3.connect(f"{os.getcwd()}/databases/key_cache.db")

    # Initialize a cursor
    dbcursor = dbconnection.cursor()

    # Get the count
    dbcursor.execute("SELECT COUNT (*) FROM database")

    # Get the result
    result = list(dbcursor)

    # Convert it into a string
    formatted_result = str(result)

    # Strip special characters
    stripped_result = formatted_result.strip("[](),")

    # return the result
    return stripped_result
