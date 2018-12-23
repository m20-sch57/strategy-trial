from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignUp(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    secondname = StringField('Second name', validators = [DataRequired()])
    username = StringField('Username*', validators = [DataRequired()])
    password = PasswordField('Password*', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')
    
class Submit(FlaskForm):
    textfield = StringField("Your code", widget = TextArea())
    submit = SubmitField('Submit')
