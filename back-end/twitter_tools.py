from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy as tw
import api
import twitter_credentials
import json

class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

#Class for streaming and processing live tweets.
class TwitterTools():
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator() 
        self.tweets = []   

    def search_tweets(self, hash_tag_list, until_date, total):
        # This handles Twitter authentification 
        #Si pasamos lista de palabras busca que esten todas, hay que buscar una por una
        
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        api = tw.API(auth)
        for key in hash_tag_list:
            query = key+" -filter:retweets"
            tweetslist = tw.Cursor(api.search, tweet_mode='extended', q=query, lang='es', until= until_date).items(total)        
            for status in tweetslist:
                self.tweets.append(status.full_text)

        return self.tweets

    def stream_tweets(self, hash_tag_list, statsObj):
        # This handles Twitter authentification and the connection to Twitter Streaming API
        listener = api.TwitterListener(statsObj, max_num_tweets=20)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list,  languages=["es"], async_ = True)
