import flask
import flask_login

app = flask.Flask(__name__)
app.secret_key = 'walnuts'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {'admin@admin.com': {'password': '111111'}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(account):
    if account not in users:
        return
    user = User()
    user.id = account
    return user


@login_manager.request_loader
def request_loader(request):
    account = request.form.get('account')
    if account not in users:
        return
    user = User()
    user.id = account
    user.is_authenticated = request.form['password'] == users[account]['password']

    return user


@app.route('/login', methods=['POST'])
def login():
    account = flask.request.form['account']
    if users.get(account, None) and flask.request.form['password'] == users[account]['password']:
        user = User()
        user.id = account
        flask_login.login_user(user)
        return flask.jsonify(code=10000, msg='login success', data=None)

    return flask.jsonify(code=20000, msg='login fail, password error', data=None)


@app.route('/book/list')
@flask_login.login_required
def book_list():
    data = ['python', 'java', 'javascript', 'go']
    return flask.jsonify(code=10000, msg='success', data=data)


if __name__ == '__main__':
    app.run()
