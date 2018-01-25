# -*- coding: utf-8 -*-
"""
Created on Wed May 31 13:52:10 2017

@author: HP-Colm
"""

# http://www.kdnuggets.com/2016/06/mining-twitter-data-python-part-2.html

import json
tweet_store = []
"""with open('python.json', 'r') as f:
        lines = f.readlines() # read only the first tweet/line
        for line in lines:
            tweet = json.loads(line) # load it as Python dict
            tweet_text = tweet["u'text'"]
            tweet_store.append(tweet_text)"""
            
with open('python.json', 'r') as f:
    for line in f:
        tweet = json.loads(line) # load it as Python dict
        tweet_text = tweet['text']
        tweet_store.append(tweet_text)
        
            
    
"""with open('python.json', 'r') as f:
        line = f.readline() # read only the first tweet/line
        tweet = json.loads(line) # load it as Python dict
        #print(json.dumps(tweet, indent=4)) # pretty-print
        tweet_text = tweet['text']
        tweet_store.append(tweet_text)"""
