from flask import Flask, request, abort
app = Flask(__name__)


@app.route('/search')
def search_api():
    search_term = get_query_arg('searchTerm')
    lat = get_float_query_arg('lat')
    lng = get_float_query_arg('lng')

    return "Welcome to /search"

def get_float_query_arg(arg_name):
    result = get_query_arg(arg_name)
    try:
        result = float(result)
    except:
        abort(400)
    return result

def get_query_arg(arg_name):
    result = request.args.get(arg_name)
    if result is None:
        abort(400)  # Bad request
    else:
        return result