from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

event_join = "join"
event_leave = "leave"
event_msg_from_srv = "message_from_srv"
event_msg_to_srv = "message_to_srv"


@app.route('/')
def root():
    return "Witam!"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    room = request.form['room']

    if not username or not room:
        return "Unexpected error"

    # Store data
    session['username'] = username
    session['room'] = room

    # Redirect to chat app
    return redirect(url_for('/chat'))

@app.route('/chat', methods=['GET'])
def chat():
    return render_template("chat.html")

@socketio.on(event_join)
def join(json):
    username = session['username']
    room = session['room']
    join_room(room)
    emit(event_msg_from_srv, {'message': f'{username} has entered and joined the room.'}, room=room)

@socketio.on(event_leave)
def leave(json):
    username = session['username']
    room = session['room']
    leave_room(room)
    session.clear()
    emit(event_msg_from_srv, {'message': f'{username} has left the room.'}, room=room)

@socketio.on(event_msg_to_srv)
def message(json):
    username = session['username']
    room = session['room']
    msg = json['message']

    emit(event_msg_from_srv, {'message': f'{username}: {msg}'}, room=room)


# def on_receive(methods=['GET', 'POST']):
#     # print("New message!")
#     pass
#
# @socketio.on('chat#1s')
# def handle_event(json, methods=['GET', 'POST']):
#     print(f'received: {json}')
#     socketio.emit('chat#1r', json)

if __name__ == "__main__":
    socketio.run(app, debug=True)
