from flask_wtf import Form
from wtforms import StringField, PasswordField, FormField, FieldList, TextAreaField
import wtforms
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class MealForm(Form):
    meal_name = StringField('Meal Name', validators=[DataRequired()])
    directions = TextAreaField('Directions')
