from re import S
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from streamer import Streamer
from classifier import Classifier as LiveClassifier
from training_classifier import Classifier as TrainingClassifier
from cortex import Cortex
import time
import os
import threading
from dotenv import load_dotenv
load_dotenv()

# https://stackoverflow.com/questions/34581255/python-flask-socketio-send-message-from-thread-not-always-working
import eventlet
eventlet.monkey_patch()

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
socketio = SocketIO(app, async_mode='eventlet')

@socketio.on('connect')
def ws_connect():
    # TODO move this logic into "top level" class and make this a one liner
    print("Socket", request.sid, "connected.")
    
    session_type = "training"
    start_time = time.time() + 5
    emit('start', start_time)

    if session_type == "training":
        classifier = TrainingClassifier(start_time)
    else: 
        classifier = LiveClassifier(start_time)

    user = {
        "license" : os.environ.get("LICENSE_KEY"),
        "client_id" : os.environ.get("CLIENT_ID"),
        "client_secret" : os.environ.get("CLIENT_SECRET"),
        "debit" : 1
    }
    cortex = Cortex(user, debug_mode=True)
    streamer = Streamer(cortex, classifier, socketio.emit)
    streamer.start()

@socketio.on('disconnect')
def ws_disconnect():
    # TODO kill threads
    print("Client", request.sid, "disconnected.")

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("index.html", data={})

if __name__ == '__main__':
    socketio.run(app)
