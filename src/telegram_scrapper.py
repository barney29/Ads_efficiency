from telethon.sync import TelegramClient
import configparser
from datetime import datetime, timezone, date, time
import pandas as pd

from sqlalchemy import create_engine

import sys
sys.path.append('../src')

from dfwrapper import DfWrapper
from db_conn import DbDriver

from utils import convert_to_df
# Read the configuration file for API credentials
config = configparser.ConfigParser()
config.read('/home/berna/playground/kifiya_ai/Ads_efficiency/config.ini')

api_id = config.get('telegram', 'api_id')
api_hash = config.get('telegram', 'api_hash')
channel = 'tikvahethiopia'

#db
dbname = config.get('database', 'dbname')
user = config.get('database', 'user')
password = config.get('database', 'password')
host = config.get('database', 'host')




#We need the data
wrapper = DfWrapper('/home/berna/playground/kifiya_ai/Ads_efficiency/data/BANKS AD DATA.csv')

#database connection
db_url = f"postgresql://{user}:{password}@{host}/{dbname}"
engine = create_engine(db_url)



# latestdate = wrapper.latest_date()
# latest = latestdate.tz_localize('UTC') #if latestdate is None else latestdate.tz_convert('UTC')


# print(f"latest: {latest}")
BOA = ['#Abyssinia_Bank', '#BoAATM', '#bankinginethiopia', 'banksinethiopia', '#BankofAbyssina', '#Apollodigitalbank', '#Apollodigitalproduct']
CBE = ['#commercialbankofethiopia', '#CBE']
GBE= ['#GBE']

ads = []
base_url = f'https://t.me/{channel}'
bankstag = [BOA, CBE, GBE]


def filter_ads_message(latest, message):
    if latest <= message.date:
        for bank in bankstag:
            for tag in bank:
                if message.text:
                    if tag in message.text:
                        # post_hour = message.date.strftime('%H:%M')
                        post_hour = message.date.strftime('%I:%M %p')
                        print(post_hour)
                                
                        if tag in BOA:
                            bank = 'BOA'
                        elif tag in CBE:
                            bank = 'CBE'
                        else:
                            bank = 'GBE'
                        
                        message_data = {
                        'Date': message.date,
                        'post_id': message.id,
                        'post_link': base_url + f'/{message.id}',
                        'views': message.views,
                        'Post Hour': post_hour,
                        'Tag': tag.strip('#'),
                        'Bank': bank,
                        'Time of day': 'NaN'
                        }
                        print("Scraped successfully")
                        return message_data  


# Connect to the Telegram client
def firstTime_scrape(latest=False):
    with TelegramClient('test', api_id, api_hash) as client:
        if latest == False:
            latest = datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        # Fetch messages starting from the destination_time
        for message in client.iter_messages(channel, offset_date=latest, reverse=True):
            # Check if the message date is within the specified range
            message_data = filter_ads_message(latest, message)
            if message_data is not None:
                ads.append(message_data)
    
    # insert to database
    df = convert_to_df(ads)
    df.to_csv('/home/berna/playground/kifiya_ai/Ads_efficiency/src/newfile.csv', mode='a+')
    df.to_sql('telegram_posts', engine, if_exists='replace', index=False)



    
todays_ads = []


today_date = date.today() 

midnight_local = datetime.combine(today_date, time())


##!! unfinished
def monitor_ads():
    with TelegramClient('test', api_id, api_hash)as client:
        for message in client.iter_messages(channel, offset_date=midnight_local, reverse=True):
             message_data = filter_ads_message(midnight_local, message)
             
             if message_data is not None:
                 todays_ads.append(message_data.post_id)
    
    #when finish reading


