from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from sklearn.feature_extraction.text import TfidfVectorizer

from spacy.lang.es.stop_words import STOP_WORDS

import spacy
import json
import csv
import os
import twitter_credentials

class stats():
    def __init__(self, file_path):
        self.tweets_list = []
        self.spacy_nlp = spacy.load("es_core_news_sm")
        self.tokens = []
        self.file_path = file_path

    def add_tweet(self, tweet):
        self.tweets_list.append(tweet)
    
    def remove_STPW(self, textTo):
        #remove stop words with spacy
        doc = self.spacy_nlp(textTo)
        tokens = [token.text for token in doc if not token.is_stop]
        return tokens
        
    def get_tweets(self):
        return self.tweets_list

    def writetoCSV(self, matrix, feature_names):
        #Write matrix in csv file, feature_names are the terms in documents
        with open(self.file_path, "w+") as csvfile:
            matriz_writer = csv.writer(csvfile)
            matriz_writer.writerow(feature_names)
            matriz_writer.writerows(matrix)

        print("Escritura completa") #delete for release

    def matriceGen(self):
        # Generate tf-idf matrix and write it in csv format
        vectorizer = TfidfVectorizer(analyzer='word', stop_words=STOP_WORDS)
        matrix = vectorizer.fit_transform(self.tweets_list)
        featureNames = vectorizer.get_feature_names()
        print(matrix.toarray())  #delete for release
        self.writetoCSV(matrix.toarray(), featureNames)

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list, statsObj):
        # This handles Twitter authentification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename, statsObj, max_num_tweets=20)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list, languages=["es"])


class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename, statsObj, max_num_tweets):
        self.counter = 0
        self.max_num_tweets = max_num_tweets
        self.fetched_tweets_filename = fetched_tweets_filename
        self.statsObj = statsObj

    def on_status(self, status):
        print(status.text)
        
    def on_data(self, data):
        try:        
            all_data = json.loads(data) #to acces like a JSON object
            self.counter += 1 #limitate number of tweets for program test  
            
            self.statsObj.add_tweet(all_data["text"])
            
            if self.counter == self.max_num_tweets:
                self.statsObj.matriceGen()
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

class Main():
    def __init__(self):
        #Inicializing variables for test and initializing program
        self.hash_tag_list = ["game of thrones", "dia de la tierra", "macri"]        
        fetched_tweets_filename = "tfidf"
        script_dir = os.path.dirname(__file__) 
        rel_path = fetched_tweets_filename + ".csv"
        file_path = os.path.join(script_dir, rel_path) 
        self.stats = stats(file_path) #class to extra functions
        self.tw_st = TwitterStreamer()
        self.tw_st.stream_tweets(file_path, self.hash_tag_list, self.stats)
# Authenticate using config.py and connect to Twitter Streaming API.

if( __name__ == '__main__'):
    Main()
"""fetched_tweets_filename = "tweets"
script_dir = os.path.dirname(__file__) 
rel_path = fetched_tweets_filename + ".txt"
file_path = os.path.join(script_dir, rel_path) 

twitter_client = TwitterClient('pycon')
print(twitter_client.get_user_timeline_tweets(1))

tweet = 'text' + all_data["text"] + '@:' + all_data["source"] + '\n'
print(data)
with open(self.fetched_tweets_filename, 'a') as tf:
   json.dump(all_data,tf) """