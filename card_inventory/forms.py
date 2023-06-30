from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    username = StringField("username", validators= [DataRequired()])
    email = StringField("email", validators= [DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField()


class CardForm(FlaskForm):
    pokemon = StringField("pokemon")
    edition = StringField("edition")
    estimated_price = DecimalField("estimated price", places = 2)
    condition = StringField("condition")
    pokemon_type = StringField("type")
    promotional = StringField("promotional")
    move_1 = StringField("move 1")
    move_2 = StringField("move 2")
    hit_points = IntegerField("hit points")
    submit_button = SubmitField()