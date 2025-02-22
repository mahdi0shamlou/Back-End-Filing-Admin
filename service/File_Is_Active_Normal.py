import time
import pymysql
import logging
from datetime import datetime, timedelta

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
                # Calculate the timestamp for 12 hours ago
                twelve_hours_ago = (datetime.now() - timedelta(hours=12)).strftime('%Y-%m-%d %H:%M:%S')

                # Fetch posts where is_active = 1 and last_checked_at is older than 12 hours
                query = """
                SELECT id, token 
                FROM Posts 
                WHERE is_active = 1 AND (last_checked_at IS NULL OR last_checked_at < %s)
                """
                cursor.execute(query, (twelve_hours_ago,))
                rows = cursor.fetchall()
                logging.info(f"Fetched {len(rows)} active files from the database.")
                return rows
        except Exception as e:
            logging.error(f"Error fetching data from the database: {e}")
            return []  # Return an empty list in case of an error
        finally:
            if connection:
                connection.close()


class GetStatusOfFileFromDivar:
    @staticmethod
    def get_status(data):
        remaining_data = []  # For files that need to be rechecked
        for i in data:
            url_for_request = 'https://api.divar.ir/v8/posts-v2/web/' + i[1]
            status, post_id = GetStatusOfFileFromDivar.fetch_status(url_for_request, i[0])
            if status == 404:
                logging.info(f"Post ID {post_id} marked as inactive (404).")
                ChangeIsActive.change_is_active(post_id)  # Update immediately for 404 status
            elif status == 429:
                logging.warning(f"Post ID {post_id} rate-limited (429), keeping in the list.")
                time.sleep(1)
                remaining_data.append(i)  # This file needs to be rechecked
            elif status == 200:
                logging.info(f"Post ID {post_id} is active (200).")
            else:
                logging.warning(f"Post ID {post_id} has unexpected status: {status}. Keeping in the list.")
                remaining_data.append(i)  # Unexpected status, recheck later

            # Update last_checked_at to the current timestamp
            UpdateLastCheckedAt.update_last_checked_at(post_id)

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


class UpdateLastCheckedAt:
    @staticmethod
    def update_last_checked_at(post_id):
        if not post_id:
            logging.info("No ID to update last_checked_at.")
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
                SET last_checked_at = NOW() 
                WHERE id = %s
                """
                cursor.execute(sql_update_query, (post_id,))
                logging.info(f"Updated last_checked_at for Post ID {post_id}.")
        except Exception as error:
            logging.error(f"Error updating last_checked_at for Post ID {post_id}: {error}")
        finally:
            if connection:
                connection.close()


def main():
    while True:  # Infinite loop
        try:
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
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            logging.info("Restarting the process after a short delay...")
            time.sleep(60)  # Wait for 1 minute before restarting in case of an error
            continue  # Restart the loop

        # Sleep for 12 hours before the next iteration
        logging.info("Sleeping for 12 hours before the next check...")
        time.sleep(12 * 60 * 60)  # Sleep for 12 hours


if __name__ == "__main__":
    main()