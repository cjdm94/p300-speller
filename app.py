from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from streamer import Streamer
from classifier import Classifier
from cortex import Cortex
import time
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
socketio = SocketIO(app)

@socketio.on('connect')
def ws_connect():
    # TODO move into "top level" class and make this a one liner
    start_time = time.time() 
    emit('start', start_time)
    classifier = Classifier(start_time)
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
    print('Client disconnected from WebSocket')

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("index.html", data={})

if __name__ == '__main__':
    socketio.run(app)
