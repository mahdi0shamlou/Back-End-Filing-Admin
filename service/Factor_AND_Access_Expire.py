import mysql.connector
from datetime import datetime


def delete_expired_access():
    # Define the current date for comparison
    current_date = datetime.now()
    print(current_date)

    # Database connection setup
    try:
        connection = mysql.connector.connect(
            host='185.190.39.252',
            user='backend',
            password='ya mahdi',
            database='BackEndFiling',
            port=3306
        )

        cursor = connection.cursor()

        try:
            # Start a transaction
            connection.start_transaction()

            # SQL query to delete expired records
            delete_query = "DELETE FROM User_Access WHERE expired_at < %s;"

            # Execute the query with the current date as a parameter
            cursor.execute(delete_query, (current_date,))

            # Commit the transaction
            connection.commit()

            print(f"Deleted {cursor.rowcount} expired access records.")

        except mysql.connector.Error as err:
            print(f"Error occurred: {err}")
            # Rollback the transaction in case of an error
            connection.rollback()

        finally:
            cursor.close()

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed.")


if __name__ == "__main__":
    delete_expired_access()
