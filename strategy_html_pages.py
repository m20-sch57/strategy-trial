import sys
sys.path.append("/")

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from app import app

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=1)
scheduler.start()

app.run(host = "0.0.0.0")

atexit.register(lambda: scheduler.shutdown())
