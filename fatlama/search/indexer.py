from annoy import AnnoyIndex


class Indexer:
    """Indexes the multidimensional embeddings to make nearest neighbours
    efficiently searchable
    This uses Spotify's Annoy library: https://github.com/spotify/annoy"""
    def __init__(self, vector_length, num_trees=10):
        """
        Create a new indexer.
        Parameters
        ----------
        vector_length - integer, how many items will be in each embedded vector
        num_trees - optional integer, default 10 - how many trees the underlying index should build
        """
        self.vector_length = vector_length
        self.num_trees = num_trees
        self.vectors = []
        self.labels = []
        self.index = None

    def index_vectors_and_data(self, vectors, data):
        """
        Create an index from the given set of vectors
        with associated data
        Parameters
        ----------
        vectors - length N list of vectors to index
        data - length N list of data corresponding to each vector (any type)

        Returns
        -------
        None
        """
        assert(len(vectors) == len(data))
        self.vectors.extend(vectors)
        self.labels.extend(data)
        self.index = self._build_index(self.vectors)

    def _build_index(self, vectors):
        index = AnnoyIndex(self.vector_length)

        for vector_num, vector in enumerate(vectors):
            index.add_item(vector_num, vector)

        index.build(self.num_trees)
        return index

    def most_similar(self, vector, num_to_return):
        """
        Returns the most similar vectors in the index to the supplied vector
        Parameters
        ----------
        vector - vector to test for similarity to
        num_to_return - number of nearby vectors to return

        Returns
        -------
        List of tuples containing (data, similarity)
        similarity is a number between 0 and 1, 1 being identical
        """
        ids, distances = self.index.get_nns_by_vector(
            vector, num_to_return, include_distances=True)

        # Maps the distance range (0,2) onto similarity (1,0)
        return [(self.labels[ids[i]], 1 - distances[i] / 2) for i in range(len(ids))]

    @staticmethod
    def create_from_database(db_client, query_embedder, vector_length):
        """
        Create an index from a database
        Parameters
        ----------
        db_client - client to supply the database data
        query_embedder - embedder to convert sentence/lat/long into vectors
        vector_length - number of elements in an embedded vector

        Returns
        -------
        Indexer which can be used to look up nearby vectors
        """
        indexer = Indexer(vector_length + 3) # +3 for the lat/lon coordinates
        vectors = []
        data = []
        for row in db_client.get_all_records():
            vectors_for_row = query_embedder.get_vectors_for_query(row['item_name'], row['lat'], row['lng'])
            vectors.extend(vectors_for_row)
            data.extend([row['id']]*len(vectors_for_row))
        indexer.index_vectors_and_data(vectors, data)
        return indexer
