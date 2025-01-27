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
        mahal_text_ret = rows[0][1]
        city_id = rows[0][4]
        #print(mahal_id)
        #print(mahal_text_ret)
        return mahal_id, mahal_text_ret, city_id

def get_type_id(text):
    if "مسکونی" in text:
        if "فروش" in text:
            return 11, "فروش آپارتمان"
        elif "اجاره" in text:
            return 21, "اجاره آپارتمان"
    elif "اداری" in text:
        if "فروش" in text:
            return 31, "فروش دفتر"
        elif "اجاره" in text:
            return 41, "اجاره دفتر"

def get_city_id(city_id):
    if city_id == 1:
        return "تهران"
    elif city_id == 2:
        return "کرج"
    elif city_id == 3:
        return "اندیشه"
    elif city_id == 4:
        return "فردیس"
    elif city_id == 5:
        return "کردان"
    elif city_id == 6:
        return "قم"


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
        #print(rows[0])
    return rows[0]

def insert_data_to_server(details, mahal_id, type_id, type_text, city_id, city_text):
    connection = mysql.connector.connect(
        host='5.34.195.27',
        user='root',
        password='ya mahdi',
        database='BackEndFiling',
        port=3306,
        auth_plugin='mysql_native_password'
    )
    if details[17] == 0 and details[18] == 0:
        param = (0, details[21][19:], 1, -12, city_id, city_text, mahal_id, mahal_text, type_id, type_text, details[1], int(details[19]), int(details[20]), details[10])
    else:
        param = (0, details[21][19:], 1, -12, city_id, city_text, mahal_id, mahal_text, type_id, type_text, details[1], int(details[17]), int(details[18]), details[10])
    query = f"""INSERT INTO Posts (is_active, token, status, `number`, city, city_text, mahal, mahal_text, `type`, type_text, title, price, price_two, meter) VALUES{param};"""
    ##print(query)
    cursor = connection.cursor()
    cursor.execute(query)
    ##print(cursor.execute(query))
    connection.commit()


if __name__ == "__main__":

    for i in range(1_990_000, 1_989_000, -1):
        try:
            #print("------------------------------------------")
            #print("section get file from arka")
            #print("------------------------------------------")

            details = get_details_from_arkafile(i)
            #for i in range(0, len(details)):
                #print(f" {details[i]} --- {i}")

            #print("------------------------------------------")
            #print("section get mahal id and text")
            #print("------------------------------------------")

            mahal_text = details[9]
            mahal_id, mahal_text, city_id = get_mahal_id(mahal_text)

            #print("------------------------------------------")
            #print("section get type id and text")
            #print("------------------------------------------")

            type_text = details[-13]
            type_id, type_text = get_type_id(type_text)
            #print(type_text)
            #print(type_id)


            #print("------------------------------------------")
            #print("section get city id and text")
            #print("------------------------------------------")

            city_text = get_city_id(city_id)
            #print(city_text)

            #print("------------------------------------------")
            #print("section save data")
            #print("------------------------------------------")
            data_for_insert = insert_data_to_server(details, mahal_id, type_id, type_text, city_id, city_text)
            print(f"index {i} succsed")
        except Exception as e:

            print(f"index {i} failed")



