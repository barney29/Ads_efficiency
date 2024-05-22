import psycopg2 as db
import configparser
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

config = configparser.ConfigParser()

config.read('/home/berna/playground/kifiya_ai/Ads_efficiency/config.ini')

# Get the details
dbname = config.get('database', 'dbname')
user = config.get('database', 'user')
password = config.get('database', 'password')
host = config.get('database', 'host')

class DbDriver():

    def connect_db(self):
        try:
            self.conn = db.connect(
            user=user,
            password=password,
            host=host,
            port=5432,
            database=dbname
            )
            self.cursor = self.conn.cursor()
            print('Database connected')
        except (Exception, db.Error) as error:
            print("Error while connecting to PostgreSQL: ", error)
    

    def create_table(self):
        try:
            self.cursor.execute("""
                        CREATE TABLE telegram_posts (
                        post_id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP,
                        views INTEGER,
                        likes INTEGER,
                        comments INTEGER
                        );
                        """)

    # Google Play Store Reviews
            self.cursor.execute("""
                CREATE TABLE app_reviews (
                    app_id SERIAL,
                    review_id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP,
                    rating INTEGER,
                    comment TEXT
                );
            """)

            # Google Play Store App Download Data
            self.cursor.execute("""
                CREATE TABLE app_downloads (
                    app_id SERIAL,
                    timestamp TIMESTAMP,
                    downloads INTEGER
                );
            """)

             # Telegram Channel Subscription Growth
            self.cursor.execute("""
                CREATE TABLE channel_subscriptions (
                    channel_id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP,
                    subscribers INTEGER
                );
            """)

            # Commit changes
            self.conn.commit()
            print("Tables created successfully!")

        except db.Error as e:
            print(f"Error creating tables: {e}")

    
    def drop_table(self, table):
        pass

    def migrate_csv_db(self, df):
        pass

    def close_db(self):
            # Close cursor and connection
            print('Database closed')
            self.cursor.close()
            self.conn.close()
