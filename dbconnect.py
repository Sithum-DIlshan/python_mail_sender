import mysql.connector
import os
from mysql.connector import errorcode
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Obtain connection string information from the portal

config = {
    "host": "ipulsedb.mysql.database.azure.com",
    "user": "master",
    "password": "insurePULSE$",
    "database": "email_data",
    "client_flags": [mysql.connector.ClientFlag.SSL],
    "ssl_ca": "DigiCertGlobalRootG2.crt.pem",
}

# Construct connection string


def insertData(email_sender: str, email_reciever: str):
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

    # Create table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS email_details (id serial PRIMARY KEY, email_sender VARCHAR(50), email_reciever VARCHAR(50), sent DATETIME);"
    )
    print("Finished creating table.")

    # Insert some data into table
    cursor.execute(
        "INSERT INTO email_details (email_sender, email_reciever, sent) VALUES (%s, %s,%s);", (email_sender, email_reciever, datetime.now())
    )
    print("Inserted", cursor.rowcount, "row(s) of data.")

    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")
