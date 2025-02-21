import time

import pymysql
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GetActiveFile:
    @staticmethod
    def get_active_files():
        try:
            connection = pymysql.connect(
                host='185.190.39.252',
                user='backend',
                password='ya mahdi',
                db='BackEndFiling',
                port=3306,
                autocommit=True
            )
            with connection.cursor() as cursor:
                cursor.execute('SELECT id, token FROM Posts WHERE is_active = 1')
                rows = cursor.fetchall()
                logging.info(f"Fetched {len(rows)} active files from the database.")
                return rows
        except Exception as e:
            logging.error(f"Error fetching data from the database: {e}")
        finally:
            if connection:
                connection.close()

class GetStatusOfFileFromDivar:
    @staticmethod
    def get_status(data):
        remaining_data = []  # برای نگهداری فایل‌هایی که باید مجدد بررسی شوند

        for i in data:
            url_for_request = 'https://api.divar.ir/v8/posts-v2/web/' + i[1]
            status, post_id = GetStatusOfFileFromDivar.fetch_status(url_for_request, i[0])

            if status == 404:
                logging.info(f"Post ID {post_id} marked as inactive (404).")
                ChangeIsActive.change_is_active(post_id)  # آپدیت فوری فایل با وضعیت 404
            elif status == 429:
                logging.warning(f"Post ID {post_id} rate-limited (429), keeping in the list.")
                time.sleep(1)
                remaining_data.append(i)  # این فایل باید مجدد بررسی شود
            elif status == 200:
                logging.info(f"Post ID {post_id} is active (200).")
            else:
                logging.warning(f"Post ID {post_id} has unexpected status: {status}. Keeping in the list.")
                remaining_data.append(i)  # وضعیت غیرمنتظره، فایل باید مجدد بررسی شود

        return remaining_data

    @staticmethod
    def fetch_status(url, post_id):
        try:
            import requests
            headers = {
                'Host': 'api.divar.ir',
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json',
                'Referer': 'https://divar.ir/',
                'Origin': 'https://divar.ir'
            }
            response = requests.get(url, headers=headers)
            logging.info(f"Checking URL: {url} - Response status: {response.status_code}")
            return response.status_code, post_id
        except Exception as e:
            logging.error(f"Error fetching {url}: {e}")
            return None, post_id

class ChangeIsActive:
    @staticmethod
    def change_is_active(post_id):
        if not post_id:
            logging.info("No ID to update.")
            return
        try:
            connection = pymysql.connect(
                host='185.190.39.252',
                user='backend',
                password='ya mahdi',
                db='BackEndFiling',
                port=3306,
                autocommit=True
            )
            with connection.cursor() as cursor:
                sql_update_query = """
                UPDATE Posts 
                SET is_active = 0 
                WHERE id = %s
                """
                cursor.execute(sql_update_query, (post_id,))
                logging.info(f"Row updated for Post ID {post_id}.")
        except Exception as error:
            logging.error(f"Error updating record for Post ID {post_id}: {error}")
        finally:
            if connection:
                connection.close()

def main():
    print('Start')
    data = GetActiveFile.get_active_files()
    num_records_fetched = len(data)

    while data:
        logging.info(f"Processing {len(data)} posts...")
        remaining_data = GetStatusOfFileFromDivar.get_status(data)
        # Update data for next iteration (only keep posts that need re-checking)
        data = remaining_data

    logging.info(f"Total records fetched from DB: {num_records_fetched}")
    logging.info("All posts have been processed.")
    print('End')

if __name__ == "__main__":
    main()