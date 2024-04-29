# Import dependencies
import sqlite3
import os


# Define check database function
def check_database(pssh: str):

    # Connect the "key_cache.db" database
    dbconnection = sqlite3.connect(f"{os.getcwd()}/databases/key_cache.db")

    # Create a cursor object
    dbcursor = dbconnection.cursor()

    # Match the entry by PSSH
    dbcursor.execute("SELECT keys FROM database WHERE pssh = :pssh", {"pssh": pssh})

    # Fetch the entries
    vaultkeys = dbcursor.fetchall()

    # Format the response if entries were found
    if vaultkeys:

        # String the dictionary entry
        vaultkey = str(vaultkeys[0])

        # Strip special characters
        stripped_vault_key = vaultkey.strip(",'()")

        # Remove double backslash with singles for new lines
        formatted_vault_key = stripped_vault_key.replace('\\n', '\n')

        # Close the connection
        dbconnection.close()

        # Return the PSSH and keys
        return pssh, formatted_vault_key

    # If no keys match the PSSH entry
    else:

        # Close the connection
        dbconnection.close()

        # Return "Not found" string.
        return "Not found"
