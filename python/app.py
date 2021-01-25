from flask import Flask, render_template
from flask_socketio import SocketIO, emit

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
    socketio.run(app)