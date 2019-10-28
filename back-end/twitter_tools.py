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
EXC_MSG = "Se ha alcanzado el limite de consultas permitidas"

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
        try:
            tweetslist = tw.Cursor(api.search, tweet_mode='extended', q=query, lang='es', until= until_date).items(total)        
            
            for status in tweetslist:
                self.tweets.append(status.full_text)
        except tw.TweepError:
            raise ExcededLimit()

        return self.tweets

    def trends(self):
        auth = self.twitter_autenticator.authenticate_twitter_app()
        api = tw.API(auth)
        try:
            arg_trends = api.trends_place(ARGENTINA_WOE_ID)
        except tw.RateLimitError:
            raise ExcededLimit()
        trends = json.loads(json.dumps(arg_trends))
        toRet = [] 
        for i in range(10):
            trend = trends[0]["trends"][i]
            toRet.append(trend["name"])
        return toRet
        
class ExcededLimit(Exception):
    #modela error al sobrepasar limite de consultas
    def __init__(self):
        Exception.__init__(self,EXC_MSG) 

