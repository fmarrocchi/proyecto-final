import os
from datetime import date
from flask import Flask, request, jsonify, abort
from flask_restful import Api, Resource
from flask_socketio import SocketIO, emit, Namespace, join_room
from threading import Thread
import search_engine
import twitter_tools
import NLTools
import json
from tweepy.streaming import StreamListener

KEYWORDS = 'keywords'
SINCE_DATE = 'since-date'
UNTIL_DATE = 'until-date'
LIMIT = 'limit'

app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app, engineio_logger=True, async_mode='eventlet')
thread = None

class Home(Resource):
    def get(self):
        print("Se encuentra en la pagina principal")
        return 'OK'
    
class Search(Resource):
    def get(self):
        #URL principal, requiere en keywords las palabras a buscar y en since-date la fecha         
        queries = request.args.getlist(KEYWORDS)          
        #s_date = request.args.get(SINCE_DATE)
        u_date = request.args.get(UNTIL_DATE)
        tweet_limit = int(request.args.get(LIMIT))
        #print(queries)
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

class Streamer(Namespace):
    def on_stream(self, data):
        print("-----data en streamer------")
        print(data)
        print(request.sid)
        join_room(request.sid)
        global thread
        if thread is None:
            thread = Thread(target=start_stream, args=("hola",5,request.sid))
            thread.start()
        print("Mando mensaje")
        #emit('streamresponse', {'stream_tweet': "hola"}, namespace='/emotions-analyzer/streaming')
        tweet_received("no se",request.sid)
        
def start_stream(keys, cant, sid):
    print("Empieza thread")
    print(keys)
    print(cant)
    twt = twitter_tools.TwitterTools() #instancia clase twitter_tools        
    twt.stream_tweets('peru', 1, sid)    #obtengo tweets en streaming

def tweet_received(text, sid):
        print("envio tweet")
        socketio.emit('streamresponse', {'stream_tweet': text}, namespace='/emotions-analyzer/streaming', room=sid)

api.add_resource(Search,'/emotions-analyzer')
api.add_resource(Home,'/')
socketio.on_namespace(Streamer('/emotions-analyzer/streaming'))

if __name__ == '__main__':
    socketio.run(app)