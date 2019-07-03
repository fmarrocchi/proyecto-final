import os
import json
import os

class Search_Engine():
    #Clase encargada de cargar el lexicon en un diccionario y mantener los datos
    #En esta clase se obtiene la cantidad de cada emocion encontrada en las palabras tokenizadas y se guarda en un diccionario de emociones
    def __init__(self):
        #diccionario global con valores iniciales para cada emocion
        self.emotions = self.crear_diccionario_emociones()

        #arreglo con porcentaje total para cada emocion
        self.porcentaje_total = []

        #lista de diccionarios con emociones calculadas para cada tweet
        self.emotions_by_tweet = []

        #ruta absoluta para probarlo
        with open(os.path.realpath('../back-end/cod_lexicon.json'), encoding="utf-8") as json_file:
            self.data = json.load(json_file)

    def getData(self):
        return self.data
    
    def getPorcentajeEmocionesTotal(self, total_tweets):
        #el arreglo retornado contiene el promedio para cada emocion
        #ordenador de la forma: Positive, Negative, Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust
        porcentaje_total = self.porcentaje_total
        #calculo porcentaje de cada emocion segun el total de tweets obtenidos     
        for e in self.emotions.keys():
            porcentaje_total.append(self.emotions[e] / total_tweets)
        return porcentaje_total

    #funcion que busca palabras en el lexicon y las cuenta
    def compute_emotions(self, tweet_tokens_list):
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
        return self.emotions_by_tweet

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
