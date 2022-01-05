# This program streams live tweets and stores them in a file called new_tweets.json
# No need to run this for analysis
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json

import credentials

import numpy as np
import pandas as pd 


class TwitterAuthenticator():
    #Handles authentication to twitter developer account
    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():

        '''
        Class for streaming live tweets
        '''
        def __init__(self):
            self.twitter_authenticator = TwitterAuthenticator()

        def stream_tweets(self, fetched_tweets_filename, keywords):
                df = pd.DataFrame()
                listener = TwitterListener(fetched_tweets_filename,df)
                auth = self.twitter_authenticator.authenticate_twitter_app()

                stream = Stream(auth, listener)

                #filter tweets
                stream.filter(track=keywords)

class TwitterListener(StreamListener):

        '''
        This is a basic listener class that just prints received tweets to stdout
        '''

        tweet_counter = 0


        def __init__(self, fetched_tweets_filename,df):
                self.fetched_tweets_filename = fetched_tweets_filename

        def on_data(self, data):
            
            #print(df)
            TwitterListener.tweet_counter+=1
            if TwitterListener.tweet_counter < 1001:
                try:
                    print(TwitterListener.tweet_counter)
                    json_data = json.loads(data)
                    print(json_data["text"])


                    with open(self.fetched_tweets_filename,'a') as tf:
                        tf.write(data)
                    #print(df)
                    return True
                except BaseException as e:
                    print("Error on data: %s" % str(e))
                            
                    #print(data)
                return True
            else:
                return False

            

        def on_error(self, status):
                if status==420:
                    return False
                print(status)



if __name__ == "__main__":
        
        #Filter and stream tweets with following characters
        filter_list = ['macbook pro','macbook','windows surface','microsoft Surface', 'Surface Pro', 'surface laptop', 'Dell xps', 'dell xps', 'dell Xps', 'xps Laptop', 'XPS', 'xps', 'Xps']
        fetched_tweets_filename = 'new_tweets.json'

        twitter_streamer = TwitterStreamer()

        twitter_streamer.stream_tweets(fetched_tweets_filename, filter_list)

        
