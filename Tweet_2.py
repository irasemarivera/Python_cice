# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 19:19:50 2020

@author: gabriel.marin
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv

#http://www.tweepy.org/
import tweepy

# Correr el programa con la instrucción: runfile('Tweet_2.py', args="Pedro")
#Get your Twitter API credentials and enter them here
consumer_key = "6i6JAMqVnXym9kF33fK6U4MIE"
consumer_secret = "hJTsiq4bUbrbEupzonxIGgv8DyYexL5kQT06uvM2ICiFHRmMVx"
access_token = "1324422374377328643-klos5jxHQNblSJwtVwv1MBwgfB5lHM"
access_secret = "2M7lLj3UwxR8gMpsXsRdFh3MsqdrC9b6ve2sZyuiy7NrE"

#method to get a user's last tweets
def get_tweets(username):

	#http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)

	#set count to however many tweets you want
	number_of_tweets = 100

	#get tweets
	tweets_for_csv = []
	for tweet in tweepy.Cursor(api.user_timeline, screen_name = username).items(number_of_tweets):
        #create array of tweet information: username, tweet id, date/time, text
		tweets_for_csv.append([username, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")])

	#write to a new csv file from the array of tweets
	outfile = "data/" + username + "_tweets.csv"
	print ("writing to " + outfile)
	with open(outfile, 'w+') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerows(tweets_for_csv)
        

#if we're running this as a script
if __name__ == '__main__':
    #Modo de uso runFile('Tweets_2.py','Pedrito')
    #get tweets for username passed at command line
    if len(sys.argv) == 2:
        get_tweets(sys.argv[1])
    else:
        print ("Error: enter one username")

    #alternative method: loop through multiple users
	# users = ['user1','user2']

	# for user in users:
	# 	get_tweets(user)