from flask import Flask, request, abort, jsonify
from fatlama.search import Indexer, DbClient, QueryEmbedder, DirectWordEmbeddingClient, Searcher
from fatlama.config import sqlite_db_path, word2vec_vector_length
from fatlama.word_embedding import WordEmbedder


class Server:
    """Main server to supply the search endpoint"""
    def __init__(self,
                 name,
                 searcher):
        """
        Create a new Server instance
        Parameters
        ----------
        name - Flask app name for this server, usually __name__
        searcher - Searcher object to use for the actual querying
        """
        self.app = Flask(name)
        self.searcher = searcher
        self.app.add_url_rule("/search", "search", self.search_api)

    def search_api(self):
        """
        Decodes the query URL, does the search lookup, and gets the
        relevant results from the database
        Returns
        -------
        Flask response as JSON
        """
        search_term = Server._get_query_arg('searchTerm')
        lat = Server._get_float_query_arg('lat')
        lng = Server._get_float_query_arg('lng')

        ids = self.searcher.get_top_results(search_term, lat, lng, 20)
        with DbClient(sqlite_db_path) as sqlite_db_client:
            results = sqlite_db_client.get_items_by_id(ids)
        return jsonify(results)

    def run(self, *argv, **kwargs):
        """
        Run the server. Takes the same parameters as Flask's app.run
        """
        self.app.run(*argv, **kwargs)

    @staticmethod
    def _get_float_query_arg(arg_name):
        """Gets an argument from the current query string as a float value"""
        result = Server._get_query_arg(arg_name)
        try:
            result = float(result)
        except:
            abort(400)
        return result

    @staticmethod
    def _get_query_arg(arg_name):
        """Gets an argument from the current query string as a string value"""
        result = request.args.get(arg_name)
        if result is None:
            abort(400)  # Bad request
        else:
            return result

    @staticmethod
    def create_default():
        """
        Creates a default server instance.
        """
        word_embedding_client = DirectWordEmbeddingClient(WordEmbedder.create_default())
        query_embedder = QueryEmbedder(word_embedding_client)

        with DbClient(sqlite_db_path) as db_client:
            indexer = Indexer.create_from_database(db_client, query_embedder, word2vec_vector_length)

        searcher = Searcher(query_embedder, indexer)

        return Server(__name__, searcher)
