from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

DB_NAME='MealTime'

DATABASE = MongoClient()[DB_NAME]
USERS_COLLECTION = DATABASE.users
MEALS_COLLECTION = DATABASE.meals
CALENDAR_COLLECTION = DATABASE.calendar
GROCERIES_COLLECTION = DATABASE.groceries

DEBUG = True
