"""

This script creates a database with the required fields if it doesn't exist already and stores the category of the article.

"""

import sqlite3
import logging

def data_with_category(df, table_name, db_filename):
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
                Category TEXT
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
                    INSERT INTO {table_name} (Title, Description, PublishedDate, URL,Category)
                    VALUES (?, ?, ?, ?,?)
                ''', (row['Title'], row['Description'], row['Published Date'], url,row['Category']))
                logging.info(f"New category added to the database: {url}")
            #else:
                #logging.info(f"Article already exists in the database: {url}")

        # Commit the changes
        conn.commit()
    except Exception as e:
        logging.error(f"Error storing new category in the database: {e}")
    finally:
        # Close the database connection
        if conn:
            conn.close()