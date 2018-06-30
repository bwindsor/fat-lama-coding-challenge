from fatlama.word_embedding import WordEmbedder
import pytest


@pytest.fixture(scope="module")
def embedder():
    return WordEmbedder.create_default()


def test_has_word(embedder):
    assert(embedder.has_word("hello") == True)
    assert(embedder.has_word("gher9tn8409thc4uq") == False)


def test_get_vector(embedder):
    vector = embedder.get_vector("hello")
    assert(type(vector) is list)
    for x in vector:
        assert(type(x) is float)
