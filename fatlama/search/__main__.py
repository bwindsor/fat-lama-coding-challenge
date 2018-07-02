from fatlama.search import Server
from fatlama.config import search_server_port

app = Server.create_default()
app.run(host='localhost', port=search_server_port, debug=True)
