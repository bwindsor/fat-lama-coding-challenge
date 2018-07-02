import math


class QueryEmbedder:
    """Converts queries (sentence + lat + lon) into vectors"""
    def __init__(self, word_embedding_client, location_weighting=1.0):
        """
        Create a QueryEmbedder
        Parameters
        ----------
        word_embedding_client - an object providing an interface to get
            a word embedding vector from a single word
        """
        self.word_embedding_client = word_embedding_client
        self.location_weighting = location_weighting

    def get_vectors_for_query(self, sentence, lat, lng):
        """
        Converts query data into an embedded vector
        Parameters
        ----------
        sentence - text to embed
        lat - latitude of query
        lng - longitude of query

        Returns
        -------
        A list of lists of floats, corresponding to vectors relevant
        to this query
        """
        vectors = self._get_vectors_for_sentence(sentence)
        for v in vectors:
            xyz = [math.sin(lat), math.cos(lat)*math.cos(lng), math.cos(lat)*math.sin(lng)]
            v.extend([x * self.location_weighting for x in xyz])
            magnitude = sum([x**2 for x in v])**0.5
            for i in range(len(v)):
                v[i] /= magnitude

        return vectors

    def _get_vectors_for_sentence(self, sentence):
        """Calls the word embedding client for each word
        in a sentence"""
        words = sentence.split()

        # Call word embedding service to get vectors per word
        vectors = [self.word_embedding_client.get_vector_for_word(w) for w in words]
        # Filter out words which were not found
        vectors = [v for v in vectors if v is not None]
        return vectors
