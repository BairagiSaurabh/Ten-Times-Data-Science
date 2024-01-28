"""
This script creates a database with the required fields and stores the data extracted.
It also ensures that no duplicate articles are stored even if we run the scripts again and again

"""

import sqlite3
import logging

def store_new_articles_in_db(df, table_name, db_filename):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_filename)

        # Check if the table exists; if not, create it
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                Title TEXT,
                Description TEXT,
                PublishedDate TEXT,
                URL TEXT PRIMARY KEY
            )
        ''')
        conn.commit()

        # Check for new articles and store them
        for index, row in df.iterrows():
            url = row['URL']
            # Check if the URL is already present in the database
            cursor.execute(f"SELECT * FROM {table_name} WHERE URL = ?", (url,))
            existing_article = cursor.fetchone()

            if existing_article is None:
                # Insert the new article into the database
                cursor.execute(f'''
                    INSERT INTO {table_name} (Title, Description, PublishedDate, URL)
                    VALUES (?, ?, ?, ?)
                ''', (row['Title'], row['Description'], row['Published Date'], url))
                logging.info(f"New article added to the database: {url}")
            #else:
                #logging.info(f"Article already exists in the database: {url}")

        # Commit the changes
        conn.commit()
    except Exception as e:
        logging.error(f"Error storing new articles in the database: {e}")
    finally:
        # Close the database connection
        if conn:
            conn.close()