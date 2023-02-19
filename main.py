from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
websocket = SocketIO(app)

@app.route('/')
def root():
    return "Witam!"

@app.route('/chat')
def chat():
    return render_template("chat.html")

def on_receive(methods=['GET', 'POST']):
    # print("New message!")
    pass

@websocket.on('chat#1s')
def handle_event(json, methods=['GET', 'POST']):
    print(f'received: {json}')
    websocket.emit('chat#1r', json)

if __name__ == "__main__":
    websocket.run(app, debug=True)
