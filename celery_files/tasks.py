from celery_config import app
from get_data import get_data_rss

@app.task
def process_rss_feed(rss_feed, table_name, db_filename):
    get_data_rss.delay(rss_feed, table_name, db_filename)
    return {"status": "success", "message": "Task submitted successfully"}
