from flask import Flask
app = Flask(__name__)


@app.route('/search')
def search_api():
    return "Welcome to /search"


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
