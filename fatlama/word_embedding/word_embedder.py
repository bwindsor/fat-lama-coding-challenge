import gensim
from fatlama.config import word2vec_model_path


class WordEmbedder():
    def __init__(self, word2vec_model_path):
        self.model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)

    def has_word(self, word):
        return word in self.model.wv

    def get_vector(self, word):
        if self.has_word(word):
            return [float(x) for x in self.model.wv[word]]
        else:
            return None

    @staticmethod
    def create_default():
        return WordEmbedder(word2vec_model_path)
