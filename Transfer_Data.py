import time
import pymysql
import mysql.connector
import sqlite3

def get_mahal_id(mahal_text):
        connection = mysql.connector.connect(
            host='5.34.195.27',
            user='root',
            password='ya mahdi',
            database='BackEndFiling',
            port=3306,
            auth_plugin='mysql_native_password'
        )
        mysql_cursor = connection.cursor()
        mysql_cursor.execute(
            f'SELECT * FROM Neighborhoods_For_Scrapper WHERE name = "{mahal_text}"')
        rows = mysql_cursor.fetchall()
        mahal_id = rows[0][3]
        print(mahal_id)
        return mahal_id

def get_details_from_arkafile(id: int):
    # Connect to the MySQL database
    mysql_connection = pymysql.connect(
        host='45.149.79.52',
        user='admin_arkafile',
        port=3306,
        password='eZtO7SOV',
        database='admin_arkafile_duplicate'
    )
    with mysql_connection.cursor() as mysql_cursor:
        mysql_cursor.execute(f"SELECT * FROM files JOIN file_categories ON files.file_category_id = file_categories.id WHERE files.id = {id};")
        rows = mysql_cursor.fetchall()
        print(rows[0])
    return rows[0]

def insert_data_to_server(details, mahal_id, type_id, type_text):
    connection = mysql.connector.connect(
        host='5.34.195.27',
        user='root',
        password='ya mahdi',
        database='BackEndFiling',
        port=3306,
        auth_plugin='mysql_native_password'
    )

    param = (0, "token", 1, -12, 1, "tehran", 68, "piroozi", 11, "sell", "title", 1000, 1000, 10)
    query = f"""INSERT INTO Posts (is_active, token, status, `number`, city, city_text, mahal, mahal_text, `type`, type_text, title, price, price_two, meter) VALUES{param};"""
    cursor = connection.cursor()
    print(cursor.execute(query))
    connection.commit()


if __name__ == "__main__":
    for i in range(1_000_000, 1000, -1):
        details = get_details_from_arkafile(i)
        for i in details:
            print(i)
        mahal_text = details[9]
        mahal_id = get_mahal_id(mahal_text)
        type_id = 11
        type_text = "تست"
        data_for_insert = insert_data_to_server(details, mahal_id, type_id, type_text)

        break

