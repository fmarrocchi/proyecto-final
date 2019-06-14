import json
import os

class Search_Engine():
    #Clase encargada de cargar el lexicon en un diccionario y mantener los datos
    #En esta clase se obtiene la cantidad de cada emocion encontrada en las palabras tokenizadas y se guarda en un diccionario de emociones
    def __init__(self):
        #diccionario con valores iniciales para cada emocion
        self.emotions = self.crear_diccionario_emociones()

        #lista de diccionarios con emociones calculadas para cada tweet
        self.emotions_by_tweet = []

        #ruta absoluta para probarlo
        with open(os.path.realpath('../back-end/cod_lexicon.json'), encoding="utf-8") as json_file:
            self.data = json.load(json_file)

    def getData(self):
        return self.data

    #funcion que busca palabras en el lexicon y las cuenta
    def buscar(self, text_list, tweet_tokens_list):
        #text_list: tokens totales
        #tweet_tokens_list: lista de listas de tokens, una por cada tweet
        for tweet_tokens in tweet_tokens_list:
            contador_tweet = self.crear_diccionario_emociones()
            #busca cada palabra de la lista recibida en el lexicon y suma en un contador total y otro para el tweet actual
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

    def total_emotion(self, emotion):
        total = 0
        if emotion in self.emotions:
            for tweet_emotions in self.emotions_by_tweet:
                if tweet_emotions.get(emotion) != 0.0:
                    total += 1
            return total
        return -1

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
