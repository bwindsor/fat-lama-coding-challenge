from fatllama.word_embedding import app
from fatllama.config import word_embedding_server_port

app.run(host='localhost', port=word_embedding_server_port)
