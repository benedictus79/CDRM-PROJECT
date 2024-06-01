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


def count_keys_devine():

    # Connect to the database
    connection = sqlite3.connect(f"{os.getcwd()}/databases/devine.db")
    cursor = connection.cursor()

    # Execute the query to count total number of keys
    cursor.execute("SELECT COUNT(kid) FROM vault")

    # Fetch the result
    total_keys = cursor.fetchone()[0]

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # return the key count
    return total_keys


def get_service_count_devine():
    # Connect to the database
    connection = sqlite3.connect(f"{os.getcwd()}/databases/devine.db")
    cursor = connection.cursor()

    # Execute the query to count unique services
    cursor.execute("SELECT COUNT(DISTINCT service) FROM vault")

    # Fetch the result
    count = cursor.fetchone()[0]

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # return the count
    return count