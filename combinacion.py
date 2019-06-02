import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import nltk
from nltk.tokenize import TweetTokenizer

import twitter_credentials
from string import punctuation

class Buscador():
    #Clase encargada de cargar el lexicon en un diccionario y mantener los datos
    #En esta clase se obtiene la cantidad de cada emocion encontrada en las 
    # palabras tokenizadas y se guarda en un diccionario de emociones
    def __init__(self):
        #diccionario con valores iniciales para cada emocion
        self.emotions = self.crear_diccionario_emociones()
        #lista de diccionarios con emociones calculadas para cada tweet
        self.emotions_by_tweet = []

        #ruta absoluta para probarlo
        with open('C:/Users/florm/Desktop/Proyecto final/proyecto final/proyecto-final/cod_lexicon.json', encoding="utf-8") as json_file:
            self.data = json.load(json_file)

    def buscar(self, text_list, tweet_tokens_list):
        for tweet_tokens in tweet_tokens_list:
            contador_tweet = self.crear_diccionario_emociones()
            #busca cada palabra de la lista recibida en el lexicon y suma en un cotnador total y otro para el tweet actual
            for word in tweet_tokens:
                if word in self.data: #si la palabra esta en el lexicon
                    emotion = self.data[word] #tomo las emociones de plutchik
                    for e in emotion:              
                        contador = self.emotions.get(e)    #tomo valor de emocion
                        contador_tweet[e]= contador_tweet.get(e) + float(emotion[e]) #sumo el valor de la emocion al contador del tweet actual 
                        self.emotions[e] = contador + float(emotion[e])  #sumo el valor de la emocion al contador de emociones global 
            self.emotions_by_tweet.append(contador_tweet)

        print("-----------cantidad de lista de emociones de tweets----------")
        print(len(self.emotions_by_tweet))

        print("-----------emotions_by_tweet--------------")
        print(self.emotions_by_tweet)

        print("--------------------Emotion items total---------------------")
        print(self.emotions.items())

    def crear_diccionario_emociones(self):
    #creo contador emociones del tweet actual e inicializo todas las emociones en 0
        emociones = dict()
        emociones ={
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
        return emociones

   
class stats():
    def __init__(self):
        #lista de tweets a tokenizar
        self.tweets_list = [] 

        #lista donde se almacenan todas las palabras tokenizadas
        self.tokens = []

        #lista donde se almacenan listas de tokens correspondientes a cada tweet
        self.tweet_tokens_list = []
        self.listatokens = [] #creo lista de tokens para tweet actual

        #lista de listas donde se guardan las emociones para cada tweet
        self.tweet_emotions_list = []

        #punctuation to remove. Crea una lista con puntuacion y digitos a remover de mi conjunto de texto (tweets)
        self.non_words = list(punctuation) 
        self.non_words.extend(['¿', '¡', '...']) 
        self.non_words.extend(map(str,range(10))) #agrega los digitos del 0 al 9 a la lista de simbolos en non_words 


    def add_tweet(self, tweet):
        if tweet not in self.tweets_list:
            self.tweets_list.append(tweet)
         
    def get_tweets(self):
        return self.tweets_list

    def get_tweet_tokens_list(self):
        return self.tweet_tokens_list

    def tokenize(self):
        #tokeniza la lista de tweets almacenada hasta el momento
        tknzr = TweetTokenizer(preserve_case=False) #Llama a la clase importada que tokeniza.preserve_case=False para poner todo en minuscula
        
        for tweet in self.tweets_list:
            tokens = tknzr.tokenize(tweet) #tweet actual tokenizado
            
            for token in tokens: 
                #sacar signos de puntuacion al tweet actual tokenizado
                if (token not in self.non_words):
                    self.tokens.append(token) #agrego token a la lista de tokens de todos los tweets
                    self.listatokens.append(token) #agrego token a la lista de tokens del tweet actual
            #agrego lista de tokens del tweet actual a la lista de tokens para cada tweet
            self.tweet_tokens_list.append(self.listatokens)
            self.listatokens =[] #vacio lista para vovler a crear una lista para el proximo tweet
           
        print("-----------------------------------cant elementos tweet_tokens------------------------------------")
        print(len(self.tweet_tokens_list))
        print(self.tweet_tokens_list[0])

        #print(self.tokens) #para ver que cuenta los emojis
    
    def get_tokens(self):
        return self.tokens

    
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    #Class for streaming and processing live tweets.
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
    #This is a basic listener that just prints received tweets to stdout.
    def __init__(self, statsObj, max_num_tweets):
        self.counter = 0
        self.max_num_tweets = max_num_tweets
        self.statsObj = statsObj

    def on_status(self, status):
        print("status----------------")
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
        self.hash_tag_list = ["macri","cfk", "cristina"]       

        #Creo una instancia de buscador (es donde se crea el mapeo)
        self.buscador = Buscador() #self es el objeto instanciado de esa clase sobre el cual se está invocando el método
        
        self.stats = stats() #class to extra functions
        self.tw_st = TwitterStreamer()  #creo intancia
        self.tw_st.stream_tweets(self.hash_tag_list, self.stats) #Obtener los tweets a partir de la instancia twitter streamer
       
        self.buscador.buscar(self.stats.get_tokens(), self.stats.get_tweet_tokens_list()) 

if __name__ == '__main__':

    print("--------------PRUEBAS---------------------")
    #Inicio
    Main()

            

 