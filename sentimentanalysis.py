#This program analyzes the tweets from file new_tweets.json
import json
import pandas as pd
from textblob import TextBlob
import re
import numpy as np
import matplotlib.pyplot as plt

import plotly.graph_objects as go

from datetime import datetime


def isMac(tweet):
	#Checks if the tweet is about mac and returns the analyzed sentiment polarity
	analysis = TextBlob(tweet)
	if 'mac' in tweet or 'Mac' in tweet or 'Macbook' in tweet:
		return analysis.sentiment.polarity
	else:
		return 0

def isSurface(tweet):
	analysis = TextBlob(tweet)
	#Checks if the tweet is about Surface Laptop and returns the analyzed sentiment polarity
	if 'surface' in tweet or 'Surface' in tweet:
		return analysis.sentiment.polarity
	else:
		return 0

def isXps(tweet):
	#Checks if the tweet is about xps Laptop and returns the analyzed sentiment polarity
	analysis = TextBlob(tweet)
	if 'xps' in tweet or 'XPS' in tweet or 'Xps' in tweet:
		return analysis.sentiment.polarity
	else:
		return 0

def tweetsCount(df):
	#Counts total number of tweets for each category and returns a dataframe with total count of each
	df3 = pd.DataFrame()
	mac_count = 0
	surface_count = 0
	xps_count = 0
	for tweet in df['tweets']:
		if 'mac' in tweet or 'Mac' in tweet or 'Macbook' in tweet:
			mac_count+=1
		if 'surface' in tweet or 'Surface' in tweet:
			surface_count+=1
		if 'xps' in tweet or 'XPS' in tweet or 'Xps' in tweet:
			xps_count+=1

	df3['laptop'] = ['mac','surface','xps']
	df3['tweet_count'] = [mac_count,surface_count,xps_count]
	return(df3)



def isCostly(tweet):
	#Check tweet sentiment regarding cost.
	if 'cost' in tweet or 'price' in tweet:
		return 1
	else:
		return 0

def batteryLife(tweet):
	#Check tweet sentiment regarding BatteryLife.
	if 'battery' in tweet or 'Battery' in tweet:
		return 1
	else:
		return 0


#Create dataframe from the streamed tweets
file1 = open('new_tweets.json', 'r')
Lines = file1.readlines()
tweets = []
created_at = []
df = pd.DataFrame()


for line in Lines:
	json_decode = json.loads(line)
	# Get text and clean the tweet
	clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", json_decode["text"]).split())
	tweets.append(clean_tweet)

	created_at.append(json_decode["created_at"])
	# Modify long date format
	df2 = pd.DataFrame([[json_decode["created_at"].replace(' +0000',''), clean_tweet]], columns=['date','tweets'])
	df = df.append(df2)

# Add Columns for different categories and populate with their polarity
df['Mac'] = np.array([isMac(tweet) for tweet in df['tweets']])
df['Surface'] = np.array([isSurface(tweet) for tweet in df['tweets']])
df['Xps'] = np.array([isXps(tweet) for tweet in df['tweets']])

print(df)

#Plot Tweet count data
tweetcount_dataframe = tweetsCount(df)
print(tweetcount_dataframe)
tweetcount_dataframe.plot.bar(x='laptop', y='tweet_count',title= 'TweetsCount', figsize=(16,7))
plt.xticks(rotation = 0)
plt.ylabel("count")
plt.show()

#Plot overall sentiment polarity data
df.plot(title = 'What is people\'s opinion?',  x='date', figsize=(16,7))
plt.xticks(rotation = 15)
plt.ylabel("sentiment_polarity")


#Plot cost polarity data
df['cost'] = np.array([isCostly(tweet) for tweet in df['tweets']])
df1 = df.loc[df['cost'] == 1]
df1.drop(columns = ['cost'], axis =1, inplace=True)
df1.plot(title = 'Worth the money?',  x='date', figsize=(16,7))
plt.xticks(rotation = 15)
plt.ylabel("sentiment_polarity")
plt.show()

#Plot batteryLife polarity data
df['batteryLife'] = np.array([batteryLife(tweet) for tweet in df['tweets']])
df2 = df.loc[df['batteryLife'] == 1]
df2.drop(columns = ['batteryLife','cost'], axis =1, inplace=True)
df2.plot(title = 'Battery Life',  x='date', figsize=(16,7))
plt.xticks(rotation = 15)
plt.ylabel("sentiment_polarity")
plt.show()






