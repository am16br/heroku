from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,HiddenField
from wtforms.validators import DataRequired,EqualTo,ValidationError
from wtforms.fields.html5 import EmailField
from app.models import User


class Loginform(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Signin')



class Signupform(FlaskForm):
    id = HiddenField()
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_check = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',message='password must be equal')])
    submit = SubmitField('Signup')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is already registered')
