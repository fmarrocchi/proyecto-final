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

    def stream_tweets(self, hash_tag_list, max_tweets, sid):
        # This handles Twitter authentification and the connection to Twitter Streaming API , is_async=True
        listener = TwitterListener(8, sid)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list,  languages=["es"])

class TwitterListener(StreamListener):
    def __init__(self, max_num_tweets, sid):
        self.counter = 0
        self.max_num_tweets = max_num_tweets
        self.tweets_list = []
        self.sid = sid

    def on_status(self, status):
        print("status----------------")
        print(status.text)
        
    def on_data(self, data):
        try:        
            all_data = json.loads(data) #to acces like a JSON object
            api.tweet_received(all_data["text"], self.sid)
            self.counter += 1 #limitate number of tweets for program test  
            
            #self.tweets_list.append(all_data["text"])
            print(self.counter)
            print(all_data["text"])
            #self.statsObj.add_tweet(all_data["text"])
            #print(all_data) #para control de que es lo que encuentra
            
            if self.counter == self.max_num_tweets:
                return False
            return True

        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)