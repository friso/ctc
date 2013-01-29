#!/usr/bin/env python
import json
import os

from flask import Flask, jsonify, make_response, redirect, request, send_from_directory
from werkzeug import SharedDataMiddleware

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/static/client.html')

@app.route('/api/ctc', methods = ['POST', 'OPTIONS'])
def api_ctc():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = request.headers.get('Access-Control-Request-Headers')

        return response

    webresponse = {}
    webresponse['cut_off'] = 42
    webresponse['terms'] = [{'term': 'Apple', 'score': 0.123}]

    response = jsonify(webresponse)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = '*'

    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True') == 'True'

    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': os.path.join(app.root_path, 'static')
    })
    app.run(host='0.0.0.0', port=port, debug=debug)
