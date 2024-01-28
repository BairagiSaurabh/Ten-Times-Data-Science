"""

This script fetches data from our database and loops through each table, applies the category allocation script
and later stores it again in the database thus, updating our database with articles having defined category

"""

from sqlalchemy import create_engine, inspect
import pandas as pd
from class_category import NewsProcessor

db_url = 'sqlite:///All_news_articles.db' # give the name of your database here.

# Create a database connection
engine = create_engine(db_url)

# Use the Inspector to get information about the database
inspector = inspect(engine)

# Fetch all table names from the database
tables = inspector.get_table_names()

# Fetch all data from each table
for table in tables:
    query = f"SELECT * FROM {table};"
    df = pd.read_sql(query, engine)
    processor_instance = NewsProcessor(df)
    processor_instance.data_cleaning()
    df1 = processor_instance.category_classification()
    df1.to_sql(f"{table}", engine, index=False, if_exists='replace')

# Close the database connection
engine.dispose()



