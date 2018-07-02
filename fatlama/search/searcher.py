from collections import OrderedDict


class Searcher:
    """Main search functionality to return results from a query"""
    def __init__(self, query_embedder, indexer):
        self.query_embedder = query_embedder
        self.indexer = indexer

    def get_top_results(self, search_term, lat, lon, num_results):
        """

        Parameters
        ----------
        search_term - string, sentence user searched for
        lat - latitude of query
        lon - longitude of query
        num_results - number of results to return

        Returns
        -------
        ids - list of item ids, sorted most likely to least likely
        """
        # Call word embedding service to get vectors
        search_vectors = self.query_embedder.get_vectors_for_query(search_term, lat, lon)

        # Deal with special case where search words were not found at all
        if len(search_vectors) == 0:
            return []

        # Match search vectors to nearest vectors from the database
        # This just joins everything into a single list showing similarities
        # between any word in the current sentence and other items
        results_to_query = round(num_results * 1.5)
        top_results = []
        while len(top_results) < num_results and results_to_query < num_results*10:
            top_results = []
            for v in search_vectors:
                top_results.extend(self.indexer.most_similar(v, results_to_query))

            # Sort by similarity, least similar first
            top_results.sort(key=lambda x: x[0])
            # Convert to dict - this keeps the first value of each key (id) and discards others
            top_results = OrderedDict(top_results)
            results_to_query *= 2

        # Get the keys, least similar will be first
        top_ids = list(top_results)
        top_ids.reverse() # Now most similar is first
        return top_ids[:num_results]  # Trim
