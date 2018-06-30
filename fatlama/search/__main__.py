from fatlama.search import app
from fatlama.config import search_server_port

app.run(host='localhost', port=search_server_port, debug=True)
