from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import glob
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

senti = SentimentIntensityAnalyzer()



def get_sentiment(text):
    score=senti.polarity_scores(text)['compound']
    if score>0.05:
        return 'Positive'
    elif score<0.05:
        return 'Negative'
    else: return 'Neutral'

from pymongo import MongoClient
client=MongoClient('localhost',27017)
db=client.tweets
collection=db.niravmodi

class StdOutListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        print('---Someone tweeted about Nirav Modi-----')
        data['sentiment']=get_sentiment(data['text'])
        print(data['text'],data['sentiment'])
        return True

    def on_error(self, status):
        print (status)


if __name__=='__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['#NiravModi'])