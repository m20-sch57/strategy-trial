import sys
sys.path.append("/")

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from app import app
from server.timer import update

scheduler = BackgroundScheduler()
scheduler.add_job(func=update, trigger="interval", seconds=1)
scheduler.start()

app.run(host="0.0.0.0", port="5057")

atexit.register(lambda: scheduler.shutdown())
