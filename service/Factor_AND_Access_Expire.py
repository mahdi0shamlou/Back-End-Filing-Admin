import mysql.connector
from datetime import datetime


def delete_expired_access():
    # Define the current date for comparison
    current_date = datetime.now()
    print(f"Current date and time: {current_date}")

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

        # Start a transaction
        connection.start_transaction()

        # SQL query to delete expired records
        delete_query = "DELETE FROM User_Access WHERE expired_at < %s;"

        # Execute the query with the current date as a parameter
        cursor.execute(delete_query, (current_date,))

        # Commit the transaction if no errors occurred
        connection.commit()
        print(f"Deleted {cursor.rowcount} expired access records.")

    except mysql.connector.Error as err:
        print(f"Database error occurred: {err}")
        if connection.is_connected():
            connection.rollback()  # Rollback on error

    finally:
        # Ensure resources are cleaned up properly
        if cursor:
            cursor.close()
            print("Cursor closed.")

        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed.")


if __name__ == "__main__":
    delete_expired_access()
