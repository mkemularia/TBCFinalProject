from wtforms.fields.numeric import FloatField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields import StringField, PasswordField, DateField, RadioField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, equal_to

class RegisterForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter Password", validators=[DataRequired(), length(min=0, max=8)])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(), equal_to("password")])


    submit = SubmitField("Register")

class ProductForm(FlaskForm):
    name = StringField("Enter Product Name", validators=[DataRequired()])
    price = FloatField("Enter Price", validators=[DataRequired()])
    img = FileField("Choose Photo", validators=[FileRequired(), FileAllowed(["png", "jpg", "jpeg"])])

    submit = SubmitField("Add")


class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()

    login = SubmitField("Log In")

class CommentForm(FlaskForm):
    text = StringField("Enter Your Comment", validators=[DataRequired()])
    product_id = SelectField("Select Product", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Add Your Comment")

