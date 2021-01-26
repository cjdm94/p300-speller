from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from classifier import Classifier
import time

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
socketio = SocketIO(app)

@socketio.on('connect')
def ws_connect():
    print('Client connected to WebSocket')
    emit('classification', "hello")

@socketio.on('disconnect')
def ws_disconnect():
    print('Client disconnected from WebSocket')

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("index.html", data={})

if __name__ == '__main__':
    # TODO 1) Connect to Cortex WebSocket
    #         - this happens in cortex.py using `websocket`

    # TODO 2) Instantiate (and train) Classifier, pass in start_time of 10s from now
    # start_time = time.time() + 10
    start_time = time.time()
    c = Classifier(start_time)
    for x in range(2701):
        prediction = c.add_sample([1,1])
        if prediction != "":
            print("PREDICTION:", prediction)
    
    # TODO 3) Instantiate streamer, and start passing in samples to the classifier

    # TODO 4) Emit a start message to the UI with the start_time

    # TODO 5) In the UI, use a timeout to delay flashing initiation until the start time

    # TODO 5) When classifier makes a prediction, send it to the UI, e.g. "x-y" (row-col, ints)
    #         - classifier needs to connect to UI via `SocketIO`

    # TODO 6) Grab the corresponding value and append it to the current value of the input box
    socketio.run(app)