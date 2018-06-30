from fatlama.word_embedding import app
from fatlama.config import word_embedding_server_port

app.run(host='localhost', port=word_embedding_server_port)
