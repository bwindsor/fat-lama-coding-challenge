## Writeup
I decided to use Word Embeddings to find which words are similar to each other. For example, many cameras in the database don't include the word camera, but words like "Nikon" and "Canon" often do. These should also appear close to the word "camera" in word embeddings so should give it as a good search result. Unfortunately this poses a scalability problem, since we'd have to compare the user's query to every item in the database to be able to find the best results.

To prevent this, I decided to index the database by calculating the embedding vector for each word in each item description, and storing this along with the database row from which it was generated.

I also decided to extend the word vector by three numbers (x,y,z coordinates) for the geographical location, scaled and renormalised by a given weighting.

I decided to store these vectors in an efficient multidimensional spacial index call [Annoy](https://github.com/spotify/annoy), open-sourced by Spotify. I discovered this by digging down into the [source code of gensim](https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/similarities/index.py), the Python library for using word2vec, to see how they did it. This allows very efficient approximate nearest neighbours queries even for large numbers of points. Unfortunately every time a point is added to the index, the index needs rebuilding. In other words, each time a new item is put on the site or removed from the site, it needs to be rebuild. It should be possible to modify the source code (or write my own equivalent using a KD-tree) which allows incremental updates without rebuilding. Within the time constrains of this example project I have left it as it is though.

When the user enters a query, I calculate the embedding vector for each word in their query (ignoring anything not in the GoogleNews embeddings dataset - this means numbers, some abbreviations, and stop words will be ignored). I then append the three numbers corresponding to the geographical coordinates with some weighting applied, determined experimentally.

For each of these vectors I then look up the most relevant results in the previously built index, and combine these in some form to come up with what the most relevant results are overall for that phrase. These ids are then used to query the database to give the full item detail.

For this I needed an id field in the database, so I added it.

I've decided to develop in Python because it's a language which I know well.

When under high load, as the code currently is it will not perform well. However, a Flask app such as this could be deployed scalably to AWS [as described here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html), or could be refactored into a `search` lambda function sitting behind an API gateway, with the database being moved to `DynamoDB` or similar.

## Setup
This code is written using Python 3.6.
1. You will need to download the [slim version of the pre-trained GoogleNews word embeddings](https://github.com/eyaler/word2vec-slim/blob/master/GoogleNews-vectors-negative300-SLIM.bin.gz) and place it in this (top level) folder. You could also use the [full version](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit), but this just makes things slower to load.
2. Unzip the model
3. Setup a new virtual environment `virtualenv venv`
4. Activate the virtual environment `venv\Scripts\activate`
5. Install development dependencies `pip install -r requirements.txt`
6. Install the `fatlama` package (and dependencies) as editable `pip install -e .`

## Architecture
There are several components to the code, each having its own purpose, and using dependency injection to join them together. Here's the hierarchy:
```
Server <- Searcher, DbClientFactory
    Searcher <- QueryEmbedder, Indexer
        QueryEmbedder <- WordEmbeddingClient
            WordEmbeddingClient <- WordEmbedder
                WordEmbedder
        Indexer
    DbClientFactory
```
Any component can be swapped out or mocked for testing purposes.


## Starting the search server
Just run
`python fatlama/search`

## Starting the word embedding server
Run
`python fatlama/word_embedding`

## Running tests
Run `pytest`

Unit test coverage is not complete, because it takes time to write extensive test coverage - I have written enough tests to demonstrate that I can test code and write testable code - including the code in `test_query_embedder.py` which demonstrates dependency injection for making code testable when there are serveral interacting components.
