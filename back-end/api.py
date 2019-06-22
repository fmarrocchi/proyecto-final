import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import search_engine
import twitter_tools
import NLTools

KEYWORDS = 'keywords'
SINCE_DATE = 'since-date'
UNTIL_DATE = 'until-date'
LIMIT = 'limit'

app = Flask(__name__, instance_relative_config=True)
api = Api(app)

class Search(Resource):
    def get(self):
        #URL principal, requiere en keywords las palabras a buscar y en since-date la fecha 
        buscador = search_engine.Search_Engine()
        queries = request.args.getlist(KEYWORDS)      
        #if queries.len == 0 return errorMessage  
        #s_date = request.args.get(SINCE_DATE)
        u_date = request.args.get(UNTIL_DATE)
        tweet_limit = int(request.args.get(LIMIT))

        twt = twitter_tools.TwitterTools()
        if tweet_limit == None:
            tweet_limit = 500
        tweets_list = twt.search_tweets(queries, u_date, tweet_limit)#obtengo tweets

        nl_tool = NLTools.NLTools()
        tokens_lists = nl_tool.tokenize(tweets_list)#tokenizo tweets
        
        analyzer = search_engine.Search_Engine()
        dicts_list = analyzer.compute_emotions(tokens_lists)#calculo emociones
        """resp = {
            "success": True,
            "message": "Emotions successfully calculated",
            "data": {
                "tweets": tweets_list,
                "emotions": dicts_list
            }            
        }"""
        resp_data = {
            "tweets" : tweets_list,
            "emotions" : dicts_list
        }
        #para permitir requests de cualquier dominio
        #evaluar reemplazar por libreria CORS, porque impide el uso de cookies
        resp = app.make_response((jsonify(resp_data), 200)) 
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return  resp

   
api.add_resource(Search,'/emotions-analyzer')

if __name__ == '__main__':
    app.run(debug=True)