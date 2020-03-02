from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app.config["MONGO_URI"] = "mongodb://localhost:27017/workflow-api"
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins="*")
mongo = PyMongo(app)

if __name__ == '__main__':
    socketio.run(app, debug=True)

userid_table=[]

for user in mongo.db.users.find({}):
    id = str(user['_id'])
    userid_table.append(id)

@socketio.on('connect')
def test_connect():
    emit('message', {'data': 'I am connected'})

@socketio.on('authenticate')
def authenticate(username, password):
    user = mongo.db.users.find_one({'name': username})
    passwordUser = user['password']
    print(passwordUser)
    response = "test"
    if user and bcrypt.check_password_hash(passwordUser, password):
        response = user
        response['_id'] = str(response['_id'])
    del response['password']
    return response

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('getMessage')
def get_message():
    send('send a message')

@socketio.on('newMessage')
def handle_new_message(text):
    print(text)