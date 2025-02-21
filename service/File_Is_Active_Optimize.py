import asyncio
import aiohttp
import aiomysql
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GetActiveFile:
    @staticmethod
    async def get_active_files():
        try:
            connection = await aiomysql.connect(
                host='185.190.39.252',
                user='backend',
                password='ya mahdi',
                db='BackEndFiling',
                port=3306,
                autocommit=True
            )
            async with connection.cursor() as cursor:
                await cursor.execute('SELECT id, token FROM Posts WHERE is_active = 1')
                rows = await cursor.fetchall()
                logging.info(f"Fetched {len(rows)} active files from the database.")
                return rows
        except Exception as e:
            logging.error(f"Error fetching data from the database: {e}")
        finally:
            if connection:
                connection.close()

class GetStatusOfFileFromDivar:
    @staticmethod
    async def get_status(data):
        remaining_data = []  # برای نگهداری فایل‌هایی که باید مجدد بررسی شوند

        async with aiohttp.ClientSession() as session:
            tasks = [GetStatusOfFileFromDivar.fetch_status(session, 'https://api.divar.ir/v8/posts-v2/web/' + i[1], i[0]) for i in data]
            results = await asyncio.gather(*tasks)

        for result in results:
            status, post_id, item = result
            if status == 404:
                logging.info(f"Post ID {post_id} marked as inactive (404).")
                await ChangeIsActive.change_is_active(post_id)  # آپدیت فوری فایل با وضعیت 404
            elif status == 429:
                logging.warning(f"Post ID {post_id} rate-limited (429), keeping in the list.")
                remaining_data.append(item)  # این فایل باید مجدد بررسی شود
            elif status == 200:
                logging.info(f"Post ID {post_id} is active (200).")
            else:
                logging.warning(f"Post ID {post_id} has unexpected status: {status}. Keeping in the list.")
                remaining_data.append(item)  # وضعیت غیرمنتظره، فایل باید مجدد بررسی شود

        return remaining_data

    @staticmethod
    async def fetch_status(session, url, post_id):
        try:
            headers = {
                'Host': 'api.divar.ir',
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json',
                'Referer': 'https://divar.ir/',
                'Origin': 'https://divar.ir'
            }
            async with session.get(url, headers=headers) as response:
                logging.info(f"Checking URL: {url} - Response status: {response.status}")
                return response.status, post_id, (post_id, url.split('/')[-1])
        except Exception as e:
            logging.error(f"Error fetching {url}: {e}")
            return None, post_id, (post_id, url.split('/')[-1])

class ChangeIsActive:
    @staticmethod
    async def change_is_active(post_id):
        if not post_id:
            logging.info("No ID to update.")
            return
        try:
            connection = await aiomysql.connect(
                host='185.190.39.252',
                user='backend',
                password='ya mahdi',
                db='BackEndFiling',
                port=3306,
                autocommit=True
            )
            async with connection.cursor() as cursor:
                sql_update_query = """
                UPDATE Posts 
                SET is_active = 0 
                WHERE id = %s
                """
                await cursor.execute(sql_update_query, (post_id,))
                logging.info(f"Row updated for Post ID {post_id}.")
        except Exception as error:
            logging.error(f"Error updating record for Post ID {post_id}: {error}")
        finally:
            if connection:
                connection.close()

async def main():
    print('Start')
    data = await GetActiveFile.get_active_files()
    num_records_fetched = len(data)

    while data:
        logging.info(f"Processing {len(data)} posts...")
        remaining_data = await GetStatusOfFileFromDivar.get_status(data)
        # Update data for next iteration (only keep posts that need re-checking)
        data = remaining_data

    logging.info(f"Total records fetched from DB: {num_records_fetched}")
    logging.info("All posts have been processed.")
    print('End')

if __name__ == "__main__":
    asyncio.run(main())