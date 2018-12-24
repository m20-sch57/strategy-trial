import storageInit
storageInit.init()

import sys
sys.path.append("/")

from app import app

app.run()
