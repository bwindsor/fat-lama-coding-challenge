from flask import Flask, request, abort, jsonify
from fatlama.search import Indexer, DbClient, QueryEmbedder, WordEmbeddingClient, DirectWordEmbeddingClient, Searcher
from fatlama.config import sqlite_db_path, word_embedding_server_port, word2vec_vector_length

app = Flask(__name__)

# word_embedding_client = WordEmbeddingClient("http://localhost:" + str(word_embedding_server_port))
word_embedding_client = DirectWordEmbeddingClient()
query_embedder = QueryEmbedder(word_embedding_client)

with DbClient(sqlite_db_path) as db_client:
    indexer = Indexer.create_from_database(db_client, query_embedder, word2vec_vector_length + 3)

searcher = Searcher(query_embedder, indexer)


@app.route('/search')
def search_api():
    search_term = get_query_arg('searchTerm')
    lat = get_float_query_arg('lat')
    lng = get_float_query_arg('lng')

    ids = searcher.get_top_results(search_term, lat, lng, 20)
    with DbClient(sqlite_db_path) as sqlite_db_client:
        results = sqlite_db_client.get_items_by_id(ids)
    return jsonify(results)


def get_float_query_arg(arg_name):
    result = get_query_arg(arg_name)
    try:
        result = float(result)
    except:
        abort(400)
    return result


def get_query_arg(arg_name):
    result = request.args.get(arg_name)
    if result is None:
        abort(400)  # Bad request
    else:
        return result