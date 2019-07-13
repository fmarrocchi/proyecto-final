import os
import json
from datetime import date
from flask import Flask, request, jsonify, abort
from flask_restful import Api, Resource
import search_engine
import twitter_tools
import NLTools

KEYWORDS = 'keywords'
SINCE_DATE = 'since-date'
UNTIL_DATE = 'until-date'
LIMIT = 'limit'
OPERATION = 'operation'

app = Flask(__name__, instance_relative_config=True)
api = Api(app)

class Search(Resource):
    def get(self):
        #URL principal, requiere en keywords las palabras a buscar y en since-date la fecha         
        queries = request.args.getlist(KEYWORDS)          
        #s_date = request.args.get(SINCE_DATE)
        u_date = request.args.get(UNTIL_DATE)
        tweet_limit = int(request.args.get(LIMIT))
        operation = int(request.args.get(OPERATION))
        if queries is None or (len(queries) is 1 and len(queries[0]) is 0):
            abort(400)
        
        if u_date is None:
            u_date = date.today()

        if tweet_limit is None:
            tweet_limit = 500

        """ buscador = search_engine.Search_Engine()
        twt = twitter_tools.TwitterTools()
        
        tweets_list = twt.search_tweets(queries, u_date, tweet_limit, operation)#obtengo tweets

        #streaming

        nl_tool = NLTools.NLTools()
        tokens_lists = nl_tool.tokenize(tweets_list)#tokenizo tweets
        
        dicts_list = buscador.compute_emotions(tokens_lists)#calculo emociones

        emocionesTotal = buscador.getPorcentajeEmocionesTotal(tweet_limit) 
        
        resp_data = {
            "tweets" : tweets_list,
            "emotions" : dicts_list,
            "porcentaje_total" : emocionesTotal
        }"""
        resp_data = {}
        with open(os.path.relpath('../back-end/datos_pruebas/datos-prueba.json'), encoding="utf-8") as file:
            resp_data = json.load(file)

        #para permitir requests de cualquier dominio
        #evaluar reemplazar por libreria CORS, porque impide el uso de cookies
        resp = app.make_response((jsonify(resp_data), 200)) 
        resp.headers['Access-Control-Allow-Origin'] = '*'
        print(resp.headers)
        return  resp

class TrendingTopics(Resource):
    def get(self):
        twt = twitter_tools.TwitterTools()
        toRet = twt.trends()
        resp_data = {
            "trending_topics": toRet
        }
        resp = app.make_response((jsonify(resp_data), 200))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
   
api.add_resource(Search,'/emotions-analyzer')
api.add_resource(TrendingTopics,'/emotions-analyzer/trends')

if __name__ == '__main__':
    app.run(debug=True)