from distutils.command.upload import upload
import os
from time import localtime, strftime
from random import randint

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    send_from_directory,
)
from flask_sqlalchemy import SQLAlchemy, model
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required,
)
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_bootstrap import Bootstrap
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import uuid as uuid

from wtform_fields import *
from model.models import User, db
from model.control_data import lst_username


load_dotenv()
database_connection = os.environ.get("DATABASE_URL")
secret_key = os.environ.get("SECRET_KEY")
UPLOAD_FOLDER = "static/images/"

app = Flask(__name__)
bootstrap = Bootstrap(app)

# config db
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_connection
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024  # 4MB max-limit.
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".gif"]
app.config["UPLOAD_PATH"] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# socketio configure
socketio = SocketIO(app)
ROOMS = ["Global", "Kuba", "Natalia", "Kamila"]

# configure flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        flash("Please login.", "danger")
        return redirect(url_for("login"))

    reg_form = RegistrationForm()
    print(f"\n\n\n test: {reg_form.validate_on_submit()} \n\n\n")
    # updated database if validation scucces
    if reg_form.validate_on_submit():
        print("\n\n\n test \n\n\n")
        firstname = reg_form.firstname.data
        lastname = reg_form.lastname.data
        password = reg_form.password.data
        email = reg_form.email.data
        picture_name = reg_form.picture_name.data
        # hash password
        hashed_pswd = pbkdf2_sha256.hash(password)
        if picture_name:
            picture_prof = secure_filename(picture_name.filename)

            pic_name = (
                str(uuid.uuid1())
                + "_"
                + (firstname + lastname)
                + "_"
                + picture_prof[-4:]
            )
            print(f"\n\n\n\n{pic_name}\n\n\n\n")

            picture_name.save(os.path.join(app.root_path, UPLOAD_FOLDER, pic_name))

            user = User(
                firstname=firstname,
                lastname=lastname,
                password=hashed_pswd,
                email=email,
                picture_name=pic_name,
            )

        else:
            user = User(
                firstname=firstname,
                lastname=lastname,
                password=hashed_pswd,
                email=email,
                picture_name="0_default.png",
            )

        # add to db

        db.session.add(user)
        db.session.commit()

        flash("Registered successfully. Please login.", "success")

        return redirect(url_for("login"))

    return render_template("register.html", form=reg_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(email=login_form.email.data).first()
        login_user(user_object)
        return redirect(url_for("chat"))

    return render_template("login.html", form=login_form)


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if not current_user.is_authenticated:
        flash("Please login.", "danger")
        return redirect(url_for("login"))

    return render_template(
        "chat.html",
        user_object=current_user,
        amount_messages=randint(1, 10),
        rooms=ROOMS,
        users=lst_username,
    )


@app.route("/profile", methods=["GET"])
def profile():
    if not current_user.is_authenticated:
        flash("Please login.", "danger")
        return redirect(url_for("login"))

    return render_template("profile.html", user_object=current_user)


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("You have logged our successfully", "success")
    return redirect(url_for("login"))


##### POPRAWKA!!!!
# @app.route("/find_friend", methods=["GET"])
# def find_friend():
#     if not current_user.is_authenticated:
#         flash("Please login.", "danger")
#         return redirect(url_for("login"))

#     find_friend = request.args.get("friend_name")
#     user = User.query.filter_by(username=find_friend).first()
#     if user == current_user.username:
#         raise ValueError
#     else:
#         context = {"friend": user}

#     return render_template(
#         "find_friend.html",
#         context=context,
#     )


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


@socketio.on("incoming-msg")
def on_message(data):
    print(data)
    msg = data["msg"]
    firstname = data["firstname"]
    room = data["room"]
    time_stamp = strftime("%b-%d %I:%M%p", localtime())
    send({"firstname": firstname, "msg": msg, "time_stamp": time_stamp}, room=room)


@socketio.on("join")
def join(data):
    join_room(data["room"])
    send(
        {"msg": data["firstname"] + " is active."},
        room=data["room"],
    )


@socketio.on("leave")
def leave(data):
    leave_room(data["room"])
    send(
        {"msg": data["firstname"] + " has left the " + data["room"] + " room."},
        room=data["room"],
    )


if __name__ == "__main__":
    socketio.run(app, debug=True)
