from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, 
    jwt_required, 
    jwt_refresh_token_required, 
    create_access_token,
    create_refresh_token,
    get_jwt_identity
)

app = Flask(__name__)
bcrypt = Bcrypt(app)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app.config["MONGO_URI"] = "mongodb://localhost:27017/workflow-api"
app.config['SECRET_KEY'] = 'secret!'
jwt = JWTManager(app)

socketio = SocketIO(app, cors_allowed_origins="*")
mongo = PyMongo(app)

def identity(payload):
    user_id = payload['identity']
    return mongo.db.users.find({ "_id": user_id})

@socketio.on('connect')
def test_connect():
    emit('message', {'data': 'I am connected'})

@socketio.on("refresh")
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return ret

@socketio.on("register")
def register():
    user = {
        "name": 'Pierre',
        "password": "test",
        "email": "test@test.fr"
    }

    errors = []

    name = mongo.db.users.find_one({'name': user['name']})
    print(name)

    if(mongo.db.users.find_one({'name': user['name']})):
        raise Exception("Username already defined")

    if(mongo.db.users.find_one({'email': user['email']})):
        raise Exception("Email already defined")

    user['password'] = bcrypt.generate_password_hash(user["password"])
    user["password"] = str(user["password"])
    mongo.db.users.insert(user)
    return "User Created"

@socketio.on_error_default
def error_handler(e):
    print('An error has occurred: ' + str(e))
    return (str(e))

@socketio.on("authenticate")
def authenticate(username, password):
    if not username:
        return "miss username parameter"
    if not password:
        return "miss password parameter"

    user = mongo.db.users.find_one({'name': username})
    passwordUser = user['password']

    if not user or not bcrypt.check_password_hash(passwordUser, password):
        return "user not found"

    name = user["name"]
    ret = {
        'access_token': create_access_token(identity=username),
        'refresh_token': create_refresh_token(identity=username)
    }
    return ret

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('getMessage')
def get_message():
    send('send a message')

@socketio.on('newMessage')
def handle_new_message(text):
    print(text)

@socketio.on("userInfos")
def get_user(name):
    current_user = get_jwt_identity()
    user = mongo.db.users.find_one({'name': name})
    del user["_id"]
    del user["password"]
    return user

if __name__ == '__main__':
    socketio.run(app, debug=True)