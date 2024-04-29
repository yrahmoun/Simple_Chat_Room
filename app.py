from flask import Flask, session, redirect, url_for, request, render_template
from flask import flash
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename
from uuid import uuid4


app = Flask(__name__)
app.secret_key = "*=secret_key=*"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./chat.db'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 32 * 5000 * 5000
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins=
                    ['http://54.236.44.155', 'http://127.0.0.1:5000'])


def allowed_file(filename):
    parts = filename.split('.')
    return parts[-1].lower() in {'png', 'jpg', 'jpeg'}


class Users(db.Model):
    """database for the users"""
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    profile_pic = db.Column(db.String(100), nullable= True)


@app.route('/register', methods=["POST", "GET"])
def register():
    """handles user registration"""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        existing_user = Users.query.filter_by(username=username).first()
        existing_email = Users.query.filter_by(email=email).first()
        file = request.files['profile_pic']
        if file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_id = str(uuid4())
            filenaùe = file_id + '_' + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = 'default.png'
        if existing_user:
            return render_template("register.html", username_error=True)
        elif existing_email:
            return render_template("register.html", email_error=True)
        else:
            new_user = Users(username=username, email=email,
                             password=password, profile_pic=filename)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
    else:
        return render_template("register.html")

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
        password = request.form["password"]
        user = Users.query.filter_by(username=username).first()
        if not user or user.password != password:
            return render_template("index.html", login_error=True)
        else:
            session["username"] = username
            return redirect(url_for("chat"))
    else:
        return render_template("index.html")

@socketio.on("connect")
def welcome():
    """sends a welcome message yo the user who joined the room"""
    username = session.get('username')
    message = "User " + username + " has joined the room!"
    socketio.emit("server_message", message)

@socketio.on("message")
def handle_message(message):
    """handles the message sent by the client and sends it back"""
    username = session.get("username")
    user = Users.query.filter_by(username=username).first()
    user_pic = user.profile_pic
    if not user_pic:
        user_pic = 'default.png'
    my_message = "YOU: " + message
    socketio.emit('my_message', {'message':my_message, 'pic': user_pic}, room=request.sid)
    message = username + ": " + message
    socketio.emit("message", {'message':message, 'pic': user_pic}, include_self=False)

@app.route("/logout")
def logout():
    """handles user logging out"""
    username = session.get("username")
    message = "User " + username + " has left the room!"
    socketio.emit("server_message", message)
    session.pop("username", None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
