import requests
from fatllama.word_embedding import WordEmbedder


class WordEmbeddingClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_vector_for_word(self, word):
        response = requests.get(self.base_url + '/vector/' + word)
        if response.status_code == 200:
            return response.json()
        else:
            return None


class DirectWordEmbeddingClient:
    def __init__(self):
        self.word_embedder = WordEmbedder.create_default()

    def get_vector_for_word(self, word):
        vector = self.word_embedder.get_vector(word)
        if vector is not None:
            vector = [float(x) for x in vector]
        return vector
