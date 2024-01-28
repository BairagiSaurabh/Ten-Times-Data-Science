
# Data Science Task

**Scripts and their usage :** (under "codes" folder)

- _store_data_without_duplicates.py_ : Given a rss feed, this script extracts title, description, date and URL from it and stores it in a database. You can also give a list of rss feeds and it will store the data in different tables of the database.

- _update_tables.py_ : This script creates a database with the required fields if it doesn't exist already and stores the data extracted. It also ensures that no duplicate articles are stored even if we run the scripts again and again.

- _class_category.py_ : This script takes in data as input and further combines the title and description, cleans the textual data and uses transformers to label the article based on the below given categories 

    ● Terrorism / protest / political unrest / riot

    ● Positive/Uplifting

    ● Natural Disasters

    ● Others

- _update_tables_with_category.py_ : This script is used to store the articles with defined categories.

- _data_to_preprocess.py_ : This script fetches data from our database and loops through each table, applies the category allocation script and later stores it again in the database thus, updating our database with articles having defined category.

**Final data obtained** : (under "Data Dump" folder)

This has all the articles with extracted data and category allotted to it. Both csv files for each articles and a database with differnt tables are present here.

**App files** : (under "celery files" folder)

- _celery_config.py_ : File to configure celery using rabbitMQ

- _get_data.py_ : This file is similar to **store_data_without_duplicates.py** and extracts and stores tha data from rss feeds.

- _tasks.py_ : This is where we define our task which would be sent to celery for the execution.

- _main_script.py_ : This is the file which we can run to start our asynchronous tasks.

