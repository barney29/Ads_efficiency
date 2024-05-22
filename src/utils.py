import pandas as pd
import numpy as np
import sys
sys.path.append('../src')

from dfwrapper import DfWrapper
from db_conn import DbDriver
wrapper = DfWrapper('/home/berna/playground/kifiya_ai/Ads_efficiency/data/BANKS AD DATA.csv')


def convert_to_df(data):
    return pd.DataFrame(data)

# db = DbDriver()
# 
# db.connect_db()
# db.create_table()
# db.close_db()

