import asyncio
import aiohttp
import aiomysql
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GetActiveFile:
    @staticmethod
    async def get_active_files():
        connection = await aiomysql.connect(
            host='5.34.195.27',
            user='root',
            password='ya mahdi',
            db='BackEndFiling',
            port=3306,
        )
        async with connection.cursor() as cursor:
            await cursor.execute('SELECT id, token FROM Posts WHERE is_active = 1 LIMIT 1000')
            rows = await cursor.fetchall()
            logging.info(f"Fetched {len(rows)} active files from the database.")
            return rows


class GetStatusOfFileFromDivar:
    @staticmethod
    async def get_status(data):
        list_id_should_change_is_active_to_false = []
        URL = 'https://api.divar.ir/v8/posts-v2/web/'


        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in data:
                url_for_request = URL + i[1]
                tasks.append(GetStatusOfFileFromDivar.fetch_status(session, url_for_request, i[0]))

            results = await asyncio.gather(*tasks)

            success_count = 0
            error_count = 0
            error_ids = []

            for result in results:
                if result[0] is None:  # If status was None (404), we append the ID
                    list_id_should_change_is_active_to_false.append(result[1])
                    error_ids.append(result[1])
                    error_count += 1
                else:
                    success_count += 1

            logging.info(f"Checked {len(data)} files: {success_count} succeeded, {error_count} failed (404).")
            if error_ids:
                logging.info(f"IDs that failed: {error_ids}")

        return list_id_should_change_is_active_to_false

    @staticmethod
    async def fetch_status(session, url, post_id):
        try:
            headers = {
                'Host': 'api.divar.ir',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
                'Accept': 'application/json, text/plain, */*',
                'Referer': 'https://divar.ir/',
                'Origin': 'https://divar.ir',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site'
            }
            async with session.get(url, headers=headers) as response:
                logging.info(f"Checking URL: {url} - Response status: {response.status}")
                if response.status == 404:
                    return None, post_id  # Return None for status and the post ID
                return response.status, post_id
        except Exception as e:
            logging.error(f"Error fetching {url}: {e}")
            return None, post_id  # Return None for status on error


class ChangeIsActive:
    @staticmethod
    async def change_is_active(list_id):
        if not list_id:
            logging.info("No IDs to update.")
            return

        connection = await aiomysql.connect(
            host='5.34.195.27',
            user='root',
            password='ya mahdi',
            db='BackEndFiling',
            port=3306,
        )

        try:
            async with connection.cursor() as cursor:
                sql_update_query = f"""
                UPDATE Posts 
                SET is_active = 0 
                WHERE id IN ({','.join(['%s'] * len(list_id))})
                """
                await cursor.execute(sql_update_query, list_id)
                await connection.commit()
                logging.info(f"{cursor.rowcount} rows updated.")

        except Exception as error:
            logging.error(f"Error updating records: {error}")
        finally:
            connection.close()


async def main():
    data = await GetActiveFile.get_active_files()

    # Log number of records fetched from DB
    num_records_fetched = len(data)

    list_id_for_edit = await GetStatusOfFileFromDivar.get_status(data)

    # Log number of checks performed and their results
    num_checks_performed = len(data)

    await ChangeIsActive.change_is_active(list_id_for_edit)

    # Print summary of operations
    logging.info(f"Total records fetched from DB: {num_records_fetched}")
    logging.info(f"Total checks performed: {num_checks_performed}")
    logging.info(f"IDs that were marked inactive: {list_id_for_edit}")


if __name__ == "__main__":
    asyncio.run(main())
