from Meal_time import app, lm
from flask import render_template,request,redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from .forms import LoginForm
from .user import User

@app.route('/index')
@login_required
def index():
	user = {'username': 'Steve'}
	posts = [{'author': {'username': 'Steve'}, 'body': 'This is a test'},
		 {'author': {'username': 'Jenny'}, 'body': 'This is also a test'}]
	return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect('/index')
        flash("Wrong username or password!", category='error')
    if current_user.is_authenticated:
        return redirect('/index')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if user == None:
        flash("User {} not found.".format(username))
        return redirect(url_for('index'))
    posts = [
      {'author': user, 'body': 'Test post #1'},
      {'author': user, 'body': 'Test post #2'},
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/meals/<username>')
@login_required
def meals(username):
    #TODO: Finish this!
    pass

@app.route('/calendar/<username>')
@login_required
def calendar(username):
    #TODO: Finish this!
    pass

@app.route('/groceries/<username>')
@login_required
def groceries(username):
    #TODO: Finish this!
    pass

@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
