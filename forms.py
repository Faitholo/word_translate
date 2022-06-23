from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, AnyOf, URL


class Question(Form):
    question = StringField(
        'question', validators=[DataRequired()]
    )
    A = StringField(
        'A', validators=[DataRequired()]
    )
    B = StringField(
        'B', validators=[DataRequired()]
    )
    C = StringField(
        'C', validators=[DataRequired()]
    )
    D = StringField(
        'D', validators=[DataRequired()]
    )
    answer = StringField(
        'answer', validators=[DataRequired()]
    )