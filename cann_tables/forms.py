from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required


class LoginForm(Form):
    username = TextField("Username", validators=[Required()])
    password = PasswordField("Password", validators=[Required()])
    remember_me = BooleanField("Remember me", default=False)
