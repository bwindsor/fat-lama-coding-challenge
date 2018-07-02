from fatlama.search import QueryEmbedder
import pytest


class MockWordEmbeddingClient:
    def get_vector_for_word(self, word):
        v = [1, 2, 3]
        norm = sum([x ** 2 for x in v]) ** 0.5
        for i in range(len(v)):
            v[i] = v[i] / norm
        return v


@pytest.fixture()
def query_embedder():
    return QueryEmbedder(MockWordEmbeddingClient(), location_weighting=0.0)


def test_query_embedder(query_embedder):
    vectors = query_embedder.get_vectors_for_query("hello", 10, 20)
    expected_vector = MockWordEmbeddingClient().get_vector_for_word("hello")
    expected_vector.extend([0, 0, 0])
    assert(vectors == [expected_vector])
