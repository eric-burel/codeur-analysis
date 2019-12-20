# Connect to the db
import atexit
import psycopg2
import os


def connect():
    connection = None

    def close_connection():
        # closing database connection.
        if(connection):
            connection.close()
            print("PostgreSQL connection is closed")

    atexit.register(close_connection)

    try:
        connection = psycopg2.connect(os.environ.get(
            "DATABASE_URL",
            "postgres://postgres:admin123@127.0.0.1:5432/postgres"
        )
        )

        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")
        cursor = connection.cursor()
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        cursor.close()
        return connection

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        os.sys.exit()
