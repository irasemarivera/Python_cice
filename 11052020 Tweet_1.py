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
consumer_key = "6i6JAMqVnXym9kF33fK6U4MIE"
consumer_secret = "hJTsiq4bUbrbEupzonxIGgv8DyYexL5kQT06uvM2ICiFHRmMVx"
access_token = "1324422374377328643-klos5jxHQNblSJwtVwv1MBwgfB5lHM"
access_secret = "2M7lLj3UwxR8gMpsXsRdFh3MsqdrC9b6ve2sZyuiy7NrE"

auth=OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

twitter_stream = Stream (auth, MyListener())
twitter_stream.filter(track=['Donald Trump'])
