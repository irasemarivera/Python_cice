# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:06:01 2020

@author: gabriel.marin
"""

import tweepy #https://github.com/tweepy/tweepy

from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

class MyListener (StreamListener):
    
    def on_data(self, data):
        try:
            with open ('data/Tweets.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error en el dato: %s" % str(e))
            return True
    def on_error(self, status):
        print(status)
        return True
    
#Credenciales del Twitter API
consumer_key = "xxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxx"
access_token = "xxxxxxxxxxxxxxxx"
access_secret = "xxxxxxxxxxxxxxxx"

auth=OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

twitter_stream = Stream (auth, MyListener())
twitter_stream.filter(track=['Donald Trump'])
