from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class AddDepForm(FlaskForm):
    title = StringField('Department Title', validators=[DataRequired()])
    chief = IntegerField('Chief id', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])

    submit = SubmitField('Submit')