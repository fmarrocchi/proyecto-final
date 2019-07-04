import sys
import tweepy as tw
from tweepy import OAuthHandler
import json

import twitter_credentials
 
ARGENTINA_WOE_ID = 23424747
auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

api = tw.API(auth)
artrends = api.trends_place(ARGENTINA_WOE_ID)

trends = json.loads(json.dumps(artrends))
 
for trend in trends[0]["trends"]:
	print (trend["name"])