
from tasks import process_rss_feed

# Example usage
rss_feed = 'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
table_name = 'BBC'
db_filename = 'try2'

process_rss_feed.delay('https://feeds.bbci.co.uk/news/world/asia/india/rss.xml', 'BBC', 'try2')
