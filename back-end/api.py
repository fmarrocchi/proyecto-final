import os
from flask import Flask, request
from flask_restful import Api, Resource
import search_engine
import twitter_tools

app = Flask(__name__, instance_relative_config=True)
api = Api(app)

class Search(Resource):
    def get(self):
        #URL principal, requiere en keywords las palabras a buscar y en since-date la fecha 
        buscador = search_engine.Search_Engine()
        queries = request.args.getlist('keywords')      
        #if queries.len == 0 return errorMessage  
        date = request.args.get('since-date')
        twt = twitter_tools.TwitterTools()
        tweets_text = twt.search_tweets(queries, date)
        #falta tokenizar la lista de tweets y luego llamar al buscador
        #la logica fue separada para mejor modularizacion
        return tweets_text, 200

   
api.add_resource(Search,'/emotions-analizer')

if __name__ == '__main__':
    app.run(debug=True)