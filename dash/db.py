# Connect to the db
import atexit
import psycopg2


def connect():
    connection = None

    def close_connection():
        # closing database connection.
        if(connection):
            connection.close()
            print("PostgreSQL connection is closed")

    atexit.register(close_connection)

    try:
        connection = psycopg2.connect(user="postgres",
                                      password="admin123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")

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
        sys.exit()
