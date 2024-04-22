from flask import Flask, session, redirect, url_for, request, render_template
from flask_socletio import SocketIO

app = Flask(__name__)
app.secret_key = "*=secret_key=*"
socketio = SocketIO(app)


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
    else
        return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, debug=true)