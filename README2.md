I'm going to use Word Embeddings to find which words are similar to each other. For example, most cameras in the database don't include the word camera, but the words "Nikon" and "Canon" would often appear close to the word "camera" in word embeddings so should give it as a good search result. Unfortunately this poses a scalability problem, since we'd have to compare the user's query to every item in the database to be able to find the best results.

To prevent this, I'm going to index the database by calculating the embedding vector for each word in each item description, and storing this along with the database row from which it was generated.

I'm also going to combine the geographical location into the embedding as two extra dimensions (lat and lon), but scaled by some amount determined by how much weighting I want to give to geographic location.

I'll then store these vectors in an efficient multidimensional spacial index call [Annoy](https://github.com/spotify/annoy), open-sourced by Spotify. This allows very efficient approximate nearest neighbours queries even for large numbers of points. Unfortunately every time a point is added to the index, the index needs rebuilding. It should be possible to modify the source code (or write my own equivalent using a KD-tree) which allows incremental updates without rebuilding. Within the time constrains of this example project I have left it as it is though.

When the user enters a query I will calculate the embedding vector for each word in their query (ignoring anything not in the GoogleNews embeddings dataset - this means numbers, some abbreviations, and stop words will be ignored).

For each word I'll then look up the most relevant results in the database, and then combine these in some form to come up with what the most relevant results are overall for that phrase.

I've decided to develop in Python because it's a language which I know well.

## Setup
This code is written using Python 3.6.
1. You will need to [download the pre-trained GoogleNews word embeddings](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit). Something else could be used but this is what I picked.
2. Setup a new virtual environment `virtualenv venv`
3. Activate the virtual environment `venv\Scripts\activate`
4. Install development dependencies `pip install -r requirements.txt`
5. Install the `fatllama` package (and dependencies) as editable `pip install -e .`

## Starting the search server
Just run
`python fatllama`