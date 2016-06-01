from flask_wtf import Form
from wtforms import StringField, PasswordField, FormField, FieldList, TextAreaField
import wtforms
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


# Using wtforms.Form instead of flask_wtf.Form because of CSRF issues
class IngredientEntryForm(wtforms.Form):
    amount = StringField('Amount')
    ingredient_name = StringField('Name')


class MealForm(Form):
    meal_name = StringField('Meal Name', validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientEntryForm), min_entries=10)
    directions = TextAreaField('Directions')
