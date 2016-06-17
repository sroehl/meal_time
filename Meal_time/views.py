from Meal_time import app, lm
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, MealForm
from .user import User
from bson.objectid import ObjectId
import pymongo
import datetime
from calendar import month_name, day_name
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
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


@app.route('/meals', methods=['GET', 'POST'])
@login_required
def meals():
    form = MealForm()
    if form.validate_on_submit():
        ingredients = []
        print(request.values)
        for value in request.values:
            print(request.values[value])
            if 'amount' in value:
                number = value.split('_')[1]
                print("number: {}".format(number))
                amount = request.values[value]
                ingredient = request.values['ingredient_' + number]
                ingredients.append({"amount": amount, "ingredient_name": ingredient})
        print(ingredients)
        meal = {}
        meal['name'] = form.meal_name.data
        meal['directions'] = form.directions.data
        meal['ingredients'] = ingredients
        meal['user'] = current_user.get_id()
        app.config['MEALS_COLLECTION'].insert(meal)
        flash("Created meal!", category='success')
        return redirect('/meals')
    meals = app.config['MEALS_COLLECTION'].find({"user": current_user.get_id()})
    # ingredients = []
    # for i in range(0, 10):
    #    ingredients.append({'1', '1'})
    return render_template('meals.html', title='Meals', username=current_user.get_id(), meals=meals, form=form)


@app.route('/meal/<meal_id>', methods=['GET', 'POST'])
@login_required
def meal(meal_id):
    meal = app.config['MEALS_COLLECTION'].find_one({"_id": ObjectId(meal_id)})
    if meal is None:
        flash("Could not find meal!", category='error')
        return redirect('/meals')

    day_of_week = datetime.datetime.now().weekday()
    beginning_day = datetime.datetime.now() - datetime.timedelta(days=day_of_week + 1)
    days = []
    for i in range(0, 7):
        raw_day = beginning_day + datetime.timedelta(days=i)
        day = month_name[raw_day.month] + " " + str(raw_day.day)
        days_since_epoch = (raw_day - datetime.datetime(1970, 1, 1)).days
        days.append({"name": day, "id": days_since_epoch})
    return render_template('single_meal.html', title=meal['name'], meal=meal, days=days)


@app.route('/calendar/<view>')
@login_required
def calendar(view):
    if view == 'day':
        days_since_epoch = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).days
        print(days_since_epoch)
        user_calendar = app.config['CALENDAR_COLLECTION'].find(
            {"days": days_since_epoch, "user": current_user.get_id()})
    if view == 'week':
        days_since_epoch = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).days
        day_of_week = datetime.datetime.now().weekday()
        low_range = days_since_epoch - (day_of_week + 1)
        high_range = days_since_epoch + (6 - day_of_week)
        user_calendar = app.config['CALENDAR_COLLECTION'].find({"days": {"$gte": low_range, "$lt": high_range},
                                                                "user": current_user.get_id()}).sort("days",
                                                                                                     pymongo.ASCENDING)
    return render_template('calendar.html', title='Calendar', username=current_user.get_id(), calendar=user_calendar)


@app.route('/groceries')
@login_required
def groceries():
    days_since_epoch = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).days
    day_of_week = datetime.datetime.now().weekday()
    low_range = days_since_epoch - (day_of_week + 1)
    high_range = days_since_epoch + (6 - day_of_week)
    user_calendar = app.config['CALENDAR_COLLECTION'].find({"days": {"$gte": low_range, "$lt": high_range},
                                                            "user": current_user.get_id(),
                                                            "bought": {"$ne": 'true'}}).sort("days",
                                                                                             pymongo.ASCENDING)
    groceries = []
    for day in user_calendar:
        meal = app.config['MEALS_COLLECTION'].find_one({"_id": day['meal_id']})
        for ingredient in meal['ingredients']:
            if ingredient['ingredient_name'] == '' or ingredient['amount'] == '':
                continue
            # TODO: Need to make units work
            # for grocery in groceries:
            #    if grocery['name'] == ingredient['ingredient_name']:
            #        grocery['amount'] += ingredient['amount']
            #        continue
            grocery = {"name": ingredient['ingredient_name'], "amount": ingredient['amount'],
                       "id": str(day['_id']) + ingredient['ingredient_name']}
            groceries.append(grocery)
    print(groceries)
    return render_template('groceries.html', title='Groceries', username=current_user.get_id(), groceries=groceries)


@app.route('/assign_meal', methods=['POST'])
@login_required
def assign_meal():
    meal_id = request.form['meal_id']
    date = request.form['date']
    if (date is not None and date != 'none') and meal_id is not None:
        meal = app.config['MEALS_COLLECTION'].find_one({"_id": ObjectId(meal_id)})
        if meal is not None:
            insert_vals = {"user": current_user.get_id(), "days": int(date), "meal_name": meal['name'],
                           "meal_id": meal_id}
            try:
                app.config['CALENDAR_COLLECTION'].insert(insert_vals)
            except pymongo.errors.DuplicateKeyError:
                pass
            return json.dumps({'status': 'success'})
    return json.dumps({'status': 'failure'})


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
