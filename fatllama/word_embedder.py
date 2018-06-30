import gensim


class WordEmbedder():
    def __init__(self, word2vec_model_path):
        self.model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)

    def has_word(self, word):
        return word in self.model.wv

    def get_vector(self, word):
        if self.has_word(word):
            return self.model.wv[word]
        else:
            return None

