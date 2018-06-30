class Searcher:
    def __init__(self, query_embedder, indexer):
        self.query_embedder = query_embedder
        self.indexer = indexer

    def get_top_results(self, search_term, lat, lon, num_results):
        # Call word embedding service to get vectors
        search_vectors = self.query_embedder.get_vectors_for_query(search_term, lat, lon)

        # Deal with special case where search words were not found at all
        if len(search_vectors) == 0:
            return []

        # Match search vectors to nearest vectors from the database
        top_results = [self.indexer.most_similar(v, num_results*2) for v in search_vectors]

        # Top results is now [ [matches for word1], [matches for word2] ]
        # Combine results from different words
        final_result = []
        for v in top_results:
            final_result.extend(v)

        return final_result
