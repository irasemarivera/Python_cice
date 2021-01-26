# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 18:14:07 2020

@author: Irasema
"""

import tweepy #https://github.com/tweepy/tweepy
import json

from pymongo import MongoClient
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

keyword = ['Black Friday']

client = MongoClient('localhost', 27017)
db = client['twitterdb']
bf = db['BF']
#bf.drop()

class MyListener (StreamListener):
    
    def on_status(self, status):
        if not hasattr(status, "retweeted_status"):
            print("Tweet id ", status.id)
            bf.insert_one(status._json)
            
    def on_error(self, status):
        print(status)
        return True
    
#Credenciales del Twitter API
consumer_key = "6i6JAMqVnXym9kF33fK6U4MIE"
consumer_secret = "hJTsiq4bUbrbEupzonxIGgv8DyYexL5kQT06uvM2ICiFHRmMVx"
access_token = "1324422374377328643-klos5jxHQNblSJwtVwv1MBwgfB5lHM"
access_secret = "2M7lLj3UwxR8gMpsXsRdFh3MsqdrC9b6ve2sZyuiy7NrE"

auth=OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
twitter_stream = Stream (auth, MyListener())
twitter_stream.filter(track=keyword, languages=["es"])