from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign In')

class SignUp(FlaskForm):
    name = StringField('Name')
    secondname = StringField('Second name')
    username = StringField('Username*', validators = [DataRequired()])
    password = PasswordField('Password*', validators = [DataRequired()])
    passwordRet = PasswordField("Retype password*", validators = [DataRequired()])
    submit = SubmitField('Sign Up')
    
class Submit(FlaskForm):
    textfield = StringField("Your code", widget = TextArea())
    submit = SubmitField('Submit')

class StrategyTester(FlaskForm):
    id1 = StringField("First ID", validators = [DataRequired()])
    id2 = StringField("Second ID", validators = [DataRequired()])
    submit = SubmitField('Submit')

class ProblemsetID(FlaskForm):
    selectfile = FileField("Select File", validators = [FileRequired()])
    submit = SubmitField('Submit')

class TournamentForm(FlaskForm):
    probId = StringField("Id of problem", validators = [DataRequired()])
    start = StringField("Tournament start time (put unix time if you want to use this)")
    submit = SubmitField("Submit")

class AddProblemForm(FlaskForm):
    selectfile = FileField("Select File", validators = [FileRequired()])
    submit = SubmitField("Submit")

class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField("Old Password", validators = [DataRequired()])
    newpassword = PasswordField("New Password", validators = [DataRequired()])
    retpassword = PasswordField("Retype password", validators = [DataRequired()])
    submit = SubmitField("Submit")

