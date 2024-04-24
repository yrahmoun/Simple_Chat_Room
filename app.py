from flask import Flask, session, redirect, url_for, request, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = "*=secret_key=*"
socketio = SocketIO(app, cors_allowed_origins='http://54.236.44.155')


@app.route('/chat')
def chat():
    """ renders the chat page """
    username = session.get("username")
    if username:
        return render_template("chat.html")
    else:
        return redirect(url_for("login"))


@app.route('/', methods=["POST", "GET"])
def login():
    """ renders the login page """
    username = session.get("username")
    if username:
        return redirect(url_for("chat"))
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
        return redirect(url_for("chat"))
    else:
        return render_template("index.html")

@socketio.on("connect")
def welcome():
    """sends a welcome message yo the user who joined the room"""
    username = session.get('username')
    message = "User " + username + " has joined the room!"
    socketio.emit("message", message)

@socketio.on("message")
def handle_message(message):
    """handles the message sent by the client and sends it back"""
    username = session.get("username")
    message = username + ": " + message
    socketio.emit("message", message)

@app.route("/logout")
def logout():
    """handles user logging out"""
    username = session.get("username")
    message = "User " + username + " has left the room!"
    socketio.emit("message", message)
    session.pop("username", None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
