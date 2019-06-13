from string import punctuation
import nltk
from nltk.tokenize import TweetTokenizer

class NLTools():
    def __init__(self):
       
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

    def get_tweet_tokens_list(self):
        return self.tweet_tokens_list

    def get_tweets_emotions_list(self):
        return self.tweet_emotions_list

    def tokenize(self, text_list):
        #tokeniza la lista de tweets almacenada hasta el momento
        tknzr = TweetTokenizer(preserve_case=False) #Llama a la clase importada que tokeniza.preserve_case=False para poner todo en minuscula
        listatokens = []

        for tweet in text_list:
            tokens = tknzr.tokenize(tweet) #tweet actual tokenizado
            
            for token in tokens: 
                #sacar signos de puntuacion al tweet actual tokenizado
                if (token not in self.non_words):
                    self.tokens.append(token) #agrego token a la lista de tokens de todos los tweets
                    listatokens.append(token) #agrego token a la lista de tokens del tweet actual
            #agrego lista de tokens del tweet actual a la lista de tokens para cada tweet
            self.tweet_tokens_list.append(listatokens)
            listatokens.clear() #vacio lista para vovler a crear una lista para el proximo tweet
           
        print("-----------------------------------cant elementos tweet_tokens------------------------------------")
        print(len(self.tweet_tokens_list))
        print(self.tweet_tokens_list[0])

        #print(self.tokens) #para ver que cuenta los emojis
    
    def get_tokens(self):
        return self.tokens
