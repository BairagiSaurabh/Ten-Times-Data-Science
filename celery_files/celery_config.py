from celery import Celery

app = Celery('Data_intern_task', broker='pyamqp://guest@localhost//', backend='rpc://')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

from tasks import *