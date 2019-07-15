from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import tweepy as tw

import twitter_credentials
import json

ARGENTINA_WOE_ID = 23424747
MODE_CONJUNCTION = 1
MODE_DISJUNCTION = 0
OP_CONJ = " AND "
OP_DISJ = " OR "

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

    def search_tweets(self, hash_tag_list, until_date, total, mode):
        # This handles Twitter authentification 
        #keywords_list: lista de palabras a buscar
        #until_date: fecha limite de busqueda
        #total: cantidad de tweets
        #mode: 1 para conjuncion, 0 para disyuncion, default is 0
        
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        api = tw.API(auth)
        query = ""
        op = OP_DISJ
        if mode is MODE_CONJUNCTION:
            op = OP_CONJ
        for key in hash_tag_list:
            if query is "":
                query = query+key
            else:
                query = query+op+key

        query = query+" -filter:retweets"
        print(query)
        tweetslist = tw.Cursor(api.search, tweet_mode='extended', q=query, lang='es', until= until_date).items(total)        
        for status in tweetslist:
            self.tweets.append(status.full_text)

        return self.tweets

    def trends(self):
        auth = self.twitter_autenticator.authenticate_twitter_app()
        api = tw.API(auth)
        arg_trends = api.trends_place(ARGENTINA_WOE_ID)
        trends = json.loads(json.dumps(arg_trends))
        toRet = [] 
        for i in range(10):
            trend = trends[0]["trends"][i]
            print(trend)
            toRet.append(trend["name"])
        return toRet

    def stream_tweets(self, hash_tag_list, statsObj):
        # This handles Twitter authentification and the connection to Twitter Streaming API
        listener = TwitterListener(statsObj, max_num_tweets=20)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        #considerar geolocalizacion
        stream.filter(track=hash_tag_list, languages=["es"])
        #stream.filter(track=[u"\U0001F602"],languages=["es"]) #para probar traer tweets con emoji

            

#This is a basic listener that just prints received tweets to stdout.
#Ver si lo vamos a utilizar, no queda muy bien
class TwitterListener(StreamListener):
    def __init__(self, statsObj, max_num_tweets):
        self.counter = 0
        self.max_num_tweets = max_num_tweets
        self.tweets_list = []
        self.statsObj = statsObj

    def on_status(self, status):
        print("status----------------")
        print(status.text)
        
    def on_data(self, data):
        try:        
            all_data = json.loads(data) #to acces like a JSON object
            self.counter += 1 #limitate number of tweets for program test  
            
            self.tweets_list.append(all_data["full_text"])
            print(all_data["full_text"])
            #self.statsObj.add_tweet(all_data["text"])
            #print(all_data["text"]) #para control de que es lo que encuentra
            
            if self.counter == self.max_num_tweets:
                #self.statsObj.writeFile()
                self.statsObj.tokenize(self.tweets_list) #tokenizar
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

#date = "2019-07-12"
#hashtag=["#macriangustiado", "#lasmentirasdecambiemos"]
#prueba = TwitterTools()
#res = prueba.search_tweets(hashtag, date, 50, 1)
#print(res)
