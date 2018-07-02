import requests
from fatlama.word_embedding import WordEmbedder


class WordEmbeddingClient:
    """Looks up word embeddings by sending HTTP requests to a
    word embedding service hosted on another server"""
    def __init__(self, base_url):
        self.base_url = base_url

    def get_vector_for_word(self, word):
        response = requests.get(self.base_url + '/vector/' + word)
        if response.status_code == 200:
            return response.json()
        else:
            return None


class DirectWordEmbeddingClient:
    """Looks up word embeddings directly from a word embedder object"""
    def __init__(self, word_embedder):
        self.word_embedder = word_embedder

    def get_vector_for_word(self, word):
        vector = self.word_embedder.get_vector(word)
        return vector
