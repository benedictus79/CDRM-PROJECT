# Import dependencies
import sqlite3
import os


# Define check database function
def check_database(pssh: str):

    # Connect to DB
    dbconnection = sqlite3.connect(f"{os.getcwd()}/databases/key_cache.db")

    # Initialize a cursor object
    dbcursor = dbconnection.cursor()

    # Find PSSH
    dbcursor.execute("SELECT keys FROM database WHERE pssh = :pssh", {"pssh": pssh})

    # Fetch all results
    vaultkeys = dbcursor.fetchall()

    # If any found
    if vaultkeys:

        # Assign variable
        vaultkey = str(vaultkeys[0])

        # Strip of sqlite special characters
        stripped_vault_key = vaultkey.strip(",'()")

        # Remove double \\ for single \
        formatted_vault_key = stripped_vault_key.replace('\\n', '\n')

        # Close the connections
        dbconnection.close()

        return formatted_vault_key

    # If no keys found
    else:

        # Close the connection
        dbconnection.close()

        # Return not found
        return "Not found"
