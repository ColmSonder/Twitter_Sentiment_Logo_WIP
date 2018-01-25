# -*- coding: utf-8 -*-
"""
Created on Wed May 24 13:36:12 2017

@author: HP-Colm
"""

# http://tweepy.readthedocs.io/en/v3.5.0/getting_started.html
# http://www.kdnuggets.com/2016/06/mining-twitter-data-python-part-1.html


import tweepy
import json
import time
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
 
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
     
api = tweepy.API(auth)

"""def process_or_store(tweet):
    print(json.dumps(tweet))
    
for friend in tweepy.Cursor(api.friends).items(1):
    process_or_store(friend._json)


for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text)
    
for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    process_or_store(status._json) 

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet.text"""
    
    

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True
 
    def on_error(self, status):
        if status == 420:
        #returning False in on_data disconnects the stream
            return False
        else:
            print(status)
            return True

 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#python'])

