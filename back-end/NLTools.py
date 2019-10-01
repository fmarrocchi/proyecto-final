from string import punctuation
import re
import nltk
from nltk.tokenize import TweetTokenizer


class NLTools():
    def __init__(self):
       
        #lista donde se almacenan todas las palabras tokenizadas
        self.tokens = []

        #lista donde se almacenan listas de tokens correspondientes a cada tweet
        self.tweet_tokens_list = []

        self.listatokens = []

        #punctuation to remove. Crea una lista con puntuacion y digitos a remover de mi conjunto de texto (tweets)
        self.non_words = list(punctuation) 
        self.non_words.extend(['¿', '¡', '...', '..']) 
        self.non_words.extend(map(str,range(10))) #agrega los digitos del 0 al 9 a la lista de simbolos en non_words 

    def get_tweet_tokens_list(self):
        return self.tweet_tokens_list

    def tokenize(self, text_list):
        #text_list: lista de tweets
        #devuelve lista de listas de tokens, cada lista representa tokenizacion del tweet de mismo indice
        #tokeniza la lista de tweets almacenada hasta el momento

        tknzr = TweetTokenizer(preserve_case=False, strip_handles=True) #Llama a la clase importada que tokeniza.preserve_case=False para poner todo en minuscula
        self.listatokens = []

        for tweet in text_list:
            no_url = re.sub(r"http\S+", "", tweet) #elimina links url
            no_hashtags = re.sub(r"#\S+", "", no_url) #elimina hashtags
            tokens = tknzr.tokenize(no_hashtags) #tweet actual tokenizado
            
            for token in tokens: 
                #sacar signos de puntuacion al tweet actual tokenizado
                if (token not in self.non_words):
                    n_token = self.reduce_lengthening(token)
                    #print(n_token)
                    self.tokens.append(n_token) #agrego token a la lista de tokens de todos los tweets
                    self.listatokens.append(token) #agrego token a la lista de tokens del tweet actual
            #agrego lista de tokens del tweet actual a la lista de tokens para cada tweet
            self.tweet_tokens_list.append(self.listatokens)
            print(self.listatokens)
            self.listatokens = [] #vacio lista para vovler a crear una lista para el proximo tweet
           
        #print("-----------------------------------cant elementos tweet_tokens------------------------------------")
        #print(len(self.tweet_tokens_list))
        #print(self.tweet_tokens_list[0])
        return self.tweet_tokens_list

    def reduce_lengthening(self, text):
        pattern = re.compile(r"(.)\1{2,}")
        return pattern.sub(r"\1\1", text)
    
    def get_tokens(self):
        return self.tokens
