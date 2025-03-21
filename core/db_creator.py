import mysql.connector
from mysql.connector import errorcode
import configparser


class DatabaseManager:
    def __init__(self, config_file='db_config.ini'):
        self.config = self.load_config(config_file)
        self.host = self.config['mysql']['host']
        self.user = self.config['mysql']['user']
        self.password = self.config['mysql']['password']
        self.database = self.config['mysql']['database']
        self.port = self.config['mysql'].getint('port')
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_users_table()
        self.close()

    def load_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist.")
            elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("User name or password is wrong.")
            else:
                print(err)

    def create_users_table(self):
        #----------------------------
        #---------- create Users_admin table
        # ----------------------------
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users_admin (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
            username VARCHAR(191) NOT NULL UNIQUE,
            password VARCHAR(191) NOT NULL,
            status INT NOT NULL,
            type INT NOT NULL,
            name VARCHAR(191),
            phone VARCHAR(191) NOT NULL UNIQUE,
            address TEXT,
            email VARCHAR(191),
            created_at TIMESTAMP NULL DEFAULT NULL,
            updated_at TIMESTAMP NULL DEFAULT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS type_users_admin (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
            name VARCHAR(191) NOT NULL UNIQUE,
            created_at TIMESTAMP NULL DEFAULT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS type_post (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
            name VARCHAR(191) NOT NULL UNIQUE,
            created_at TIMESTAMP NULL DEFAULT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS file_note (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
            file_id BIGINT(20) UNSIGNED NOT NULL,
            note TEXT NOT NULL,
            FOREIGN KEY (file_id) REFERENCES Posts(id) ON DELETE CASCADE,
            created_at TIMESTAMP NULL DEFAULT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_note (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
            user_id BIGINT(20) UNSIGNED NOT NULL
            note VARCHAR(191) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            created_at TIMESTAMP NULL DEFAULT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS moshaver_number (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
            phone VARCHAR(191) NOT NULL,
            created_at TIMESTAMP NULL DEFAULT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    db_manager = DatabaseManager()
