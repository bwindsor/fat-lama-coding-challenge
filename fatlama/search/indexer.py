from annoy import AnnoyIndex


class Indexer:
    def __init__(self, vector_length, num_trees=10):
        self.vector_length = vector_length
        self.num_trees = num_trees
        self.vectors = []
        self.labels = []
        self.index = None

    def index_vectors_and_data(self, vectors, data):
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
        ids, distances = self.index.get_nns_by_vector(
            vector, num_to_return, include_distances=True)

        # Maps the distance range (0,2) onto similarity (1,0)
        return [(self.labels[ids[i]], 1 - distances[i] / 2) for i in range(len(ids))]

    @staticmethod
    def create_from_database(db_client, query_embedder, vector_length):
        indexer = Indexer(vector_length)
        vectors = []
        data = []
        for row in db_client.get_all_records():
            vectors_for_row = query_embedder.get_vectors_for_query(row['item_name'], row['lat'], row['lng'])
            vectors.extend(vectors_for_row)
            data.extend([row['id']]*len(vectors_for_row))
        indexer.index_vectors_and_data(vectors, data)
        return indexer
