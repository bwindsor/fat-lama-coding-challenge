from fatllama.search import Indexer
import pytest


def test_indexer_basic():
    indexer = Indexer(3)
    indexer.index_vectors_and_data([[1,0,0], [0,1,0], [0,0,1]], ['a',7,[8, 'hi']])
    result = indexer.most_similar([1,0,0], 3)
    assert(result == [
        ('a', 1),
        (7, pytest.approx(1 - (2**0.5)/2)),
        ([8, 'hi'], pytest.approx(1 - (2**0.5)/2))
    ])
