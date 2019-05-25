import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import nltk
from nltk.tokenize import TweetTokenizer

import twitter_credentials
from string import punctuation

class Buscador():
    #clase encargada de cargar el lexicon en un diccionario y mantener los datos
    def __init__(self):
        #diccionario con valores iniciales para cada emocion
        self.emotions = dict()
        self.emotions = {
            "Positive": 0.0, 
            "Negative": 0.0,
            "Anger": 0.0,
            "Anticipation": 0.0,
            "Disgust": 0.0,
            "Fear": 0.0,
            "Joy": 0.0,
            "Sadness": 0.0,
            "Surprise": 0.0,
            "Trust": 0.0
        }
        #ruta absoluta para probarlo
        with open('C:/Users/scrap/Documents/Proyecto final/Proyecto/archivos_lexicon/cod_lexicon.json', encoding="utf-8") as json_file:
            self.data = json.load(json_file)

    def buscar(self, text_list):
        #busca cada palabra de la lista recibida en el lexicon e imprime los valores de las emociones para 
        #cada palabra
        for word in text_list:
            if word in self.data:
                emotion = self.data[word]
                print(word)
                for e in emotion:                    
                    contador = self.emotions.get(e)                    
                    self.emotions[e] = contador + float(emotion[e])  
                    print(self.emotions.get(e))                  
                    
        print(self.emotions.items())
   
class stats():
    def __init__(self):
        #lista de tweets a tokenizar
        self.tweets_list = [] 
        #lista que va a contener todas las palabras
        self.tokens = []
        #punctuation to remove
        self.non_words = list(punctuation) 
        self.non_words.extend(['¿', '¡', '...']) 
        self.non_words.extend(map(str,range(10))) #no se exactamente que hace

    def add_tweet(self, tweet):
        if tweet not in self.tweets_list:
            self.tweets_list.append(tweet)
         
    def get_tweets(self):
        return self.tweets_list

    def tokenize(self):
        #tokeniza la lista de tweets almacenada hasta el momento
        tknzr = TweetTokenizer(preserve_case=False)
        for tweet in self.tweets_list:
            tokens = tknzr.tokenize(tweet)
            for token in tokens:
                #sacar signos de puntuacion
                if (token not in self.non_words):
                    self.tokens.append(token)
        print(self.tokens) #para ver que cuenta los emojis
    
    def get_tokens(self):
        return self.tokens

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, hash_tag_list, statsObj):
        # This handles Twitter authentification and the connection to Twitter Streaming API
        listener = TwitterListener(statsObj, max_num_tweets=20)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        #considerar geolocalizacion
        stream.filter(track=hash_tag_list, languages=["es"])
        #stream.filter(track=[u"\U0001F602"],languages=["es"]) #para probar traer tweets con emoji


class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, statsObj, max_num_tweets):
        self.counter = 0
        self.max_num_tweets = max_num_tweets
        self.statsObj = statsObj

    def on_status(self, status):
        print(status.text)
        
    def on_data(self, data):
        try:        
            all_data = json.loads(data) #to acces like a JSON object
            self.counter += 1 #limitate number of tweets for program test  
            
            self.statsObj.add_tweet(all_data["text"])
            print(all_data["text"]) #para control de que es lo que encuentra
            
            if self.counter == self.max_num_tweets:
                #self.statsObj.writeFile()
                self.statsObj.tokenize() #tokenizar
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
        #puse esas porque siempre aparece algo
        self.hash_tag_list = ["macri","cfk", "cristina"]       

        self.buscador = Buscador()
        
        self.stats = stats() #class to extra functions
        self.tw_st = TwitterStreamer()
        self.tw_st.stream_tweets(self.hash_tag_list, self.stats)
        self.buscador.buscar(self.stats.get_tokens())

if __name__ == '__main__':

    print("--------------PRUEBAS---------------------")
    #Inicio
    Main()

            

 