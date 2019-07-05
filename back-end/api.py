import os
from datetime import date
from flask import Flask, request, jsonify, abort
from flask_restful import Api, Resource
from flask_socketio import SocketIO, emit,Namespace
import search_engine
import twitter_tools
import NLTools
import json
from tweepy.streaming import StreamListener

KEYWORDS = 'keywords'
SINCE_DATE = 'since-date'
UNTIL_DATE = 'until-date'
LIMIT = 'limit'

app = Flask(__name__, instance_relative_config=True)
api = Api(app)
socketio = SocketIO(app)
ROOMS = {}

class Search(Resource):
    def get(self):
        #URL principal, requiere en keywords las palabras a buscar y en since-date la fecha         
        queries = request.args.getlist(KEYWORDS)          
        #s_date = request.args.get(SINCE_DATE)
        u_date = request.args.get(UNTIL_DATE)
        tweet_limit = int(request.args.get(LIMIT))
        print(queries)
        if queries is None or (len(queries) is 1 and len(queries[0]) is 0):
            abort(400)
        
        if u_date is None:
            u_date = date.today()

        if tweet_limit is None:
            tweet_limit = 500

        buscador = search_engine.Search_Engine()
        twt = twitter_tools.TwitterTools()
        
        tweets_list = twt.search_tweets(queries, u_date, tweet_limit)#obtengo tweets      

        nl_tool = NLTools.NLTools()
        tokens_lists = nl_tool.tokenize(tweets_list)#tokenizo tweets
        
        dicts_list = buscador.compute_emotions(tokens_lists)#calculo emociones

        emocionesTotal = buscador.getPorcentajeEmocionesTotal(tweet_limit)
        
        resp_data = {
            "tweets" : tweets_list,
            "emotions" : dicts_list,
            "porcentaje_total" : emocionesTotal
        }
        #para permitir requests de cualquier dominio
        #evaluar reemplazar por libreria CORS, porque impide el uso de cookies
        resp = app.make_response((jsonify(resp_data), 200)) 
        resp.headers['Access-Control-Allow-Origin'] = '*'
        print(resp.headers)
        return  resp     

class StreamListener(StreamListener):
    def on_status(self, status):
        TwitterListener.tweet_received(status.text)        

class MyCustomNamespace(Namespace):
    def on_stream(self, data):
        print("-----data en my custom space------")
        print(data)
        twt = twitter_tools.TwitterTools() #instancia clase twitter_tools        
        streaming = twt.stream_tweets(data['keywords'], data['limit'])    #obtengo tweets en streaming

    def on_disconnect(self):
        pass

    @staticmethod
    def tweet_received(text):
        emit('tweet_response', {'text': text}, broadcast=True, namespace='/motions-analyzer/streaming')
    
        
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
            
            self.tweets_list.append(all_data["text"])
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

api.add_resource(Search,'/emotions-analyzer')
socketio.on_namespace(MyCustomNamespace('/emotions-analyzer/streaming'))

if __name__ == '__main__':
    socketio.run(app)
    #app.run(host='0.0.0.0',port=5000)
    #app.run(debug=True)