from flask import Flask, render_template, request, redirect, url_for
import flask_login
import json


app = Flask(__name__)
app.secret_key = 'WWI0n77PiCvpwpI9ca3Y'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


users = json.load(open("users.json", "r"))


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username

    user.is_authenticated = request.form['password'] == users[username]['password']

    return user


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Bad login"

        if password == users[username]['password']:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for('protected'))

    return "Bad login"


@app.route('/protected')
@flask_login.login_required
def protected():
    return "protected"


@app.route('/test')
def test():
    return users


if __name__ == '__main__':
    app.run()
