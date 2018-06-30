import pytest
from fatlama.search import app


@pytest.fixture
def client():
    return app.test_client()


def test_valid_query(client):
    rv = client.get("/search?searchTerm=a&lat=0&lng=0")
    assert(rv.status_code == 200)


@pytest.mark.parametrize("query_string", [
    "searchTerm=a&lat=0",
    "searchTerm=a&lng=0",
    "lat=0&lng=0",
])
def test_query_parts_missing(client, query_string):
    rv = client.get("/search?" + query_string)
    assert(rv.status_code == 400)
