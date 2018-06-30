import math


class QueryEmbedder:
    def __init__(self, word_embedding_client):
        self.word_embedding_client = word_embedding_client

    def get_vectors_for_query(self, sentence, lat, lng):
        vectors = self._get_vectors_for_sentence(sentence)
        for v in vectors:
            xyz = [math.sin(lat), math.cos(lat)*math.cos(lng), math.cos(lat)*math.sin(lng)]
            weighting = 0.1
            v.extend([x * weighting for x in xyz])
            magnitude = sum([x**2 for x in v])**0.5
            for i in range(len(v)):
                v[i] /= magnitude

        return vectors

    def _get_vectors_for_sentence(self, sentence):
        words = sentence.split()

        # Call word embedding service to get vectors per word
        vectors = [self.word_embedding_client.get_vector_for_word(w) for w in words]
        # Filter out words which were not found
        vectors = [v for v in vectors if v is not None]
        return vectors
