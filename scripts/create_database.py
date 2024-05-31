# import dependencies
import sqlite3
import os


# Check to see if the database already exists, if not create a databases folder, and create the database.
def create_database():

    # Check to see if the "databases" directory exists, if not creates it
    if "databases" not in os.listdir():
        os.makedirs('databases')

    # Change to the databases directory
    os.chdir("databases")

    # Check to see if a database exists in databases directory, if not create it
    if not os.path.isfile("key_cache.db"):

        # Connect / Create "key_cache.db"
        dbconnection = sqlite3.connect("key_cache.db")

        # Create cursor
        dbcursor = dbconnection.cursor()

        # Create table through the cursor
        dbcursor.execute('CREATE TABLE IF NOT EXISTS "DATABASE" ( "pssh" TEXT, "keys" TEXT, PRIMARY KEY("pssh") )')

        # Close the connection
        dbconnection.close()

    # Check to see if a database exists in databases directory, if not create it
    if not os.path.isfile("users.db"):
        # Connect / Create "key_cache.db"
        dbconnection = sqlite3.connect("users.db")

        # Create cursor
        dbcursor = dbconnection.cursor()

        # Create table through the cursor
        dbcursor.execute('CREATE TABLE IF NOT EXISTS "DATABASE" ( "username" TEXT, "hashedpassword" TEXT, '
                             '"cached_keys" TEXT, PRIMARY KEY("username") )')

        # Close the connection
        dbconnection.close()

    # Check to see if a database exists in databases directory, if not create it
    if not os.path.isfile("devine.db"):
        dbconnection = sqlite3.connect("devine.db")
        dbcursor = dbconnection.cursor()
        dbcursor.execute('CREATE TABLE IF NOT EXISTS "vault" ( "service" TEXT, "kid" TEXT, '
                             '"key" TEXT, PRIMARY KEY("kid") )')

    # Change back to root directory
    os.chdir(os.path.join(os.getcwd(), ".."))