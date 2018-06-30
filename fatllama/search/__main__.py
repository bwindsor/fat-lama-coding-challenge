from fatllama.search import app
from fatllama.config import search_server_port

app.run(host='localhost', port=search_server_port, debug=True)
