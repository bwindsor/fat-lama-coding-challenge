from fatllama.word_embedding import WordEmbedder
from flask import Flask
from flask import jsonify
app = Flask(__name__)


word_embedder = WordEmbedder.create_default()


@app.route('/vector/<word>')
def vector_api(word):
    vector = word_embedder.get_vector(word)
    if vector is None:
        return "", 404
    else:
        return jsonify([float(x) for x in vector]), 200
