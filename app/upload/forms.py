from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,HiddenField,TextAreaField
from wtforms.validators import DataRequired,ValidationError
from flask_wtf.file import FileRequired,FileField,FileAllowed

class Uploadfeed(FlaskForm):
    name = StringField('pets name', validators=[DataRequired()])
    pic = FileField('Pets pic')
    about = TextAreaField('Tell us something about your pet',validators=[DataRequired()])
    submit = SubmitField('UPLOAD')

