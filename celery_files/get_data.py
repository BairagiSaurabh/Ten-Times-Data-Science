from update_tables import store_new_articles_in_db
from bs4 import BeautifulSoup
import requests
import pandas as pd
from dateutil import parser
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO

def get_data_rss(rss_feed,table_name,db_filename):
    try:
        # Fetch the RSS feed
        url = requests.get(rss_feed)
        url.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.RequestException as e:
        logging.error(f"Error fetching RSS feed: {e}")
        return None

    try:
        soup = BeautifulSoup(url.content, 'xml')
        items = soup.find_all('item')
    except Exception as e:
        logging.error(f"Error parsing RSS feed content: {e}")
        return None

    titles = []
    contents = []
    published_dates = []
    urls = []

    for entry in items:
        title = entry.title.text if entry.title else ''
        content_tag = entry.find('description')
        if content_tag:
            p_tags = content_tag.get_text()
            if '<p>' in p_tags:
                soup_description = BeautifulSoup(p_tags, 'html.parser')
                content = soup_description.get_text().replace("Read more...", "").strip()
            else:
                content = content_tag.text
        else:
            content = ""

        published_date_str = entry.pubDate.text if entry.pubDate else ''

        # Check if pubDate is not empty before attempting to parse
        if published_date_str:
            try:
                published_date = parser.parse(published_date_str).strftime("%d %b %Y %H:%M:%S")
            except ValueError as e:
                logging.error(f"Error parsing published date: {e}")
                published_date = ''
        else:
            published_date = ''

        url = entry.link.text if entry.link else ''

        # Append data to lists
        titles.append(title)
        contents.append(content)
        published_dates.append(published_date)
        urls.append(url)

    # Create a DataFrame
    df = pd.DataFrame({
        'Title': titles,
        'Description': contents,
        'Published Date': published_dates,
        'URL': urls
    })

    df.drop_duplicates(subset=['URL'], inplace=True)
    store_new_articles_in_db(df,table_name,db_filename)
    return {"status": "success", "message": "Task completed successfully"}