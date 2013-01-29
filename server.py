import zmq
import server_messages_pb2
import sys
import json

from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response

app = Flask(__name__)

ctx = zmq.Context()

@app.route('/', methods = ['POST', 'OPTIONS'])
def default_request():
	if request.method == 'OPTIONS':
		response = make_response()
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = 'POST'
		response.headers['Access-Control-Allow-Headers'] = request.headers['Access-Control-Request-Headers']

		return response


	zmq_socket = ctx.socket(zmq.REQ)
	zmq_socket.connect('tcp://localhost:1234')

	zmq_request = server_messages_pb2.TermRequest()
	zmq_request.request_id_major = 42
	zmq_request.request_id_minor = 42
	zmq_request.text = request.json['text']
	zmq_request.type = server_messages_pb2.TermRequest.REPLY_ONLY
	zmq_socket.send(zmq_request.SerializeToString())
	
	msg = zmq_socket.recv()

	zmq_response = server_messages_pb2.TermResponse()
	zmq_response.ParseFromString(msg)

	webresponse = {}
	webresponse['cut_off'] = zmq_response.suggested_cut_off
	webresponse['terms'] = [{'term':t.term, 'score':t.score} for t in zmq_response.terms]

	response = jsonify(webresponse)
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Methods'] = 'POST'
	response.headers['Access-Control-Allow-Headers'] = '*'
	
	return response

if __name__ == '__main__':
	app.run(debug = True)
