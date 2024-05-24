"""

"""
import sys
sys.path.append('../src')

from telegram_scrapper import firstTime_scrape
from db_conn import DbDriver
isFirstTime = True


if isFirstTime:
    db = DbDriver()
    db.run_setup()
    firstTime_scrape()
else:
    pass
