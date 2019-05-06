from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, length
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
    probId = StringField("Write over problem with id... (leave empty if you want to create a new one)")
    submit = SubmitField("Submit")

class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField("Old Password", validators = []) #this field isn't used sometimes
    newpassword = PasswordField("New Password", validators = [DataRequired()])
    retpassword = PasswordField("Retype password", validators = [DataRequired()])
    submit = SubmitField("Submit")

class MessageForm(FlaskForm):
    contentField = TextAreaField("", validators = [DataRequired(), length(max=10000)])
    submit = SubmitField("Post")

