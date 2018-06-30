import pytest
from fatllama import app


@pytest.fixture
def client():
    return app.test_client()


def test_search_endpoint_exists(client):
    rv = client.get("/search")
    assert(rv.status_code == 200)
