import asyncio
import aiomysql
import time


async def get_mahal_id(mahal_text):
    async with aiomysql.connect(
            host='5.34.195.27',
            user='root',
            password='ya mahdi',
            db='BackEndFiling',
            port=3306,
            autocommit=True
    ) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                'SELECT * FROM Neighborhoods_For_Scrapper WHERE name = %s', (mahal_text,))
            rows = await cursor.fetchall()
            if rows:
                mahal_id = rows[0][3]
                mahal_text_ret = rows[0][1]
                city_id = rows[0][4]
                return mahal_id, mahal_text_ret, city_id
    return None, None, None


async def get_type_id(text):
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
    return None, None


async def get_city_id(city_id):
    cities = {
        1: "تهران",
        2: "کرج",
        3: "اندیشه",
        4: "فردیس",
        5: "کردان",
        6: "قم"
    }
    return cities.get(city_id, None)


async def get_details_from_arkafile(id):
    async with aiomysql.connect(
            host='45.149.79.52',
            user='admin_arkafile',
            password='eZtO7SOV',
            db='admin_arkafile_duplicate',
            port=3306,
    ) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"""
                SELECT * FROM files 
                JOIN file_categories ON files.file_category_id = file_categories.id 
                WHERE files.id = %s;""", (id,))
            rows = await cursor.fetchall()
            if rows:
                return rows[0]
    return None


async def insert_data_to_server(details, mahal_id, type_id, type_text, city_id, city_text):
    async with aiomysql.connect(
            host='5.34.195.27',
            user='root',
            password='ya mahdi',
            db='BackEndFiling',
            port=3306,
            autocommit=True
    ) as connection:
        async with connection.cursor() as cursor:
            if details[17] == 0 and details[18] == 0:
                param = (
                0, details[21][19:], details[23], details[22], city_id, city_text, mahal_id, details[9], type_id, type_text, details[1],
                int(details[19]), int(details[20]), details[10])
            else:
                param = (
                0, details[21][19:], details[23], details[22], city_id, city_text, mahal_id, details[9], type_id, type_text, details[1],
                int(details[17]), int(details[18]), details[10])

            query = f"""INSERT INTO Posts (is_active, token, status, `number`, city,
                       city_text, mahal, mahal_text, `type`, type_text,
                       title, price, price_two, meter) VALUES {param};"""
            await cursor.execute(query)


async def main(start, end):
    success_count = 0
    failure_count = 0
    errors = []

    start_time = time.time()  # Start timing

    tasks = []
    for i in range(start, end, -1):
        tasks.append(process_index(i))

    # Await all tasks concurrently
    results = await asyncio.gather(*tasks)

    for result in results:
        if result is True:
            success_count += 1
        else:
            failure_count += 1
            errors.append(result)

    end_time = time.time()  # End timing

    print(f"Total Successes: {success_count}")
    print(f"Total Failures: {failure_count}")
    print(f"Errors: {errors}")
    print(f"Total Time Taken: {end_time - start_time:.2f} seconds")


async def process_index(i):
    try:
        details = await get_details_from_arkafile(i)
        if not details:
            print(f"index {i} no details found")
            return False

        mahal_text = details[9]
        mahal_id, mahal_text_ret, city_id = await get_mahal_id(mahal_text)

        type_text = details[-13]
        type_id, type_text_ret = await get_type_id(type_text)

        city_text = await get_city_id(city_id)

        await insert_data_to_server(details, mahal_id, type_id, type_text_ret, city_id, city_text)
        print(f"index {i} succeeded")

        return True

    except Exception as e:
        error_message = f"index {i} failed: {e}"
        print(error_message)
        return error_message


if __name__ == "__main__":
    for i in range(15000, 1992541, 100):
        asyncio.run(main(i+100, i))
