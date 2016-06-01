from Meal_time import app, lm
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm
from .user import User


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
            return redirect('/meals')
        flash("Wrong username or password!", category='error')
    if current_user.is_authenticated:
        return redirect('/meals')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user')
@login_required
def user():
    return render_template('user.html', user=current_user.get_id())


@app.route('/meals')
@login_required
def meals():
    meals={}
    return render_template('meals.html', title='Meals', username=current_user.get_id(), meals=meals)


@app.route('/calendar')
@login_required
def calendar():
    calendar={}
    return render_template('calendar.html', title='Calendar', username=current_user.get_id(), calendar=calendar)


@app.route('/groceries')
@login_required
def groceries():
    groceries={}
    return render_template('groceries.html', title='Groceries', username=current_user.get_id(), groceries=groceries)


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
