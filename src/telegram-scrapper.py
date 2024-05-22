from telethon.sync import TelegramClient
import configparser
from datetime import datetime, timezone
import pandas as pd


import sys
sys.path.append('../src')
from dfwrapper import DfWrapper
from utils import convert_to_df
# Read the configuration file for API credentials
config = configparser.ConfigParser()
config.read('/home/berna/playground/kifiya_ai/Ads_efficiency/config.ini')

api_id = config.get('telegram', 'api_id')
api_hash = config.get('telegram', 'api_hash')
channel = 'tikvahethiopia'


#We need the data
wrapper = DfWrapper('/home/berna/playground/kifiya_ai/Ads_efficiency/data/BANKS AD DATA.csv')


latestdate = wrapper.latest_date()
latest = latestdate.tz_localize('UTC') #if latestdate is None else latestdate.tz_convert('UTC')

today = datetime(2024, 5, 21, 0, 0, 0, tzinfo=timezone.utc)
print(f"latest: {latest}")
bankstag = ['#Abyssinia_Bank', '#BoAATM', '#bankinginethiopia', 'banksinethiopia', '#BankofAbyssina', '#Apollodigitalbank', '#Apollodigitalproduct']

ads = []
base_url = f'https://t.me/{channel}'

# Connect to the Telegram client
with TelegramClient('test', api_id, api_hash) as client:
    # Fetch messages starting from the destination_time
    for message in client.iter_messages(channel, offset_date=latest, reverse=True):
        # Check if the message date is within the specified range
        
        if latest <= message.date:
            for bank in bankstag:
                if message.text:
                    if bank in message.text:
                        post_hour = message.date.strftime('%H:%M')
                        message_data = {
                            'Date': message.date,
                            'Post link': base_url + f'/{message.id}',
                            'View': message.views,
                            'Post Hour': post_hour,
                            'Bank': bank.strip('#'),
                            'Time of day': 'NaN'
                            }
                        ads.append(message_data)

                # else:
                #     with open('./log.txt', 'a') as f:
                #         f.write(f'No Bank Ad for today: {datetime.now()}\n')
            # print(f'No ads for today: {message.date}')
    

#converting to data frame
df = convert_to_df(ads)

df.to_csv('/home/berna/playground/kifiya_ai/Ads_efficiency/data/BANKS AD DATA.csv', mode='a', header=False, index=False)