# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:14:48 2020

@author: Irasema
"""

from pymongo import MongoClient
import random
import string
client = MongoClient('localhost', 27017)

db = client['prueba2']
tweets = db['tweets']
tweets.drop()

usuarios = [("gabrimarin", 1420), ("herminia", 5320), ("calixto", 332), ("melibea", 411)]

n = 100

for i in range (1, n+1):
    tweet = {}
    tweet['_id'] = i
    tweet['text'] = ''.join(random.choices(string.ascii_uppercase, k = 10))
    u = {}
    u['nick'], u['seguidores'] = random.choice(usuarios)
    tweet['usuario'] = u
    tweet['RT'] = i>1 and random.choice([False, True])
    if tweet ['RT'] and i>1:
        tweet ['origen'] = random.randrange(1, i)
    m = random.sample(usuarios, random.randrange(0, len(usuarios)))
    tweet['mentions'] = [nick for nick, _ in m]
    tweets.insert_one(tweet)

