from flask import Flask, request, abort, jsonify
from fatlama.search import Indexer, DbClient, QueryEmbedder, DirectWordEmbeddingClient, Searcher
from fatlama.config import sqlite_db_path, word2vec_vector_length


class Server:
    def __init__(self,
                 name,
                 searcher):
        self.app = Flask(name)
        self.searcher = searcher
        self.app.add_url_rule("/search", "search", self.search_api)

    def search_api(self):
        search_term = Server._get_query_arg('searchTerm')
        lat = Server._get_float_query_arg('lat')
        lng = Server._get_float_query_arg('lng')

        ids = self.searcher.get_top_results(search_term, lat, lng, 20)
        with DbClient(sqlite_db_path) as sqlite_db_client:
            results = sqlite_db_client.get_items_by_id(ids)
        return jsonify(results)

    def run(self, *argv, **kwargs):
        self.app.run(*argv, **kwargs)

    @staticmethod
    def _get_float_query_arg(arg_name):
        result = Server._get_query_arg(arg_name)
        try:
            result = float(result)
        except:
            abort(400)
        return result

    @staticmethod
    def _get_query_arg(arg_name):
        result = request.args.get(arg_name)
        if result is None:
            abort(400)  # Bad request
        else:
            return result

    @staticmethod
    def create_default():
        word_embedding_client = DirectWordEmbeddingClient()
        query_embedder = QueryEmbedder(word_embedding_client)

        with DbClient(sqlite_db_path) as db_client:
            indexer = Indexer.create_from_database(db_client, query_embedder, word2vec_vector_length)

        searcher = Searcher(query_embedder, indexer)

        return Server(__name__, searcher)
