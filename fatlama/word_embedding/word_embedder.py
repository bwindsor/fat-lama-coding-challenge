import gensim
from fatlama.config import word2vec_model_path


class WordEmbedder():
    """Manages word2vec word embeddings"""
    def __init__(self, word2vec_model_path):
        self.model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)

    def has_word(self, word):
        """Checks if a given word is in the model
        Returns boolean"""
        return word in self.model.wv

    def get_vector(self, word):
        """Converts a word into an embedded vector
        Returns None if the word is not found"""
        if self.has_word(word):
            return [float(x) for x in self.model.wv[word]]
        else:
            return None

    @staticmethod
    def create_default():
        return WordEmbedder(word2vec_model_path)
