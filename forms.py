from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, AnyOf, URL

class Language(Form):
    lang = StringField(
        'lang', validators=[DataRequired()]
    )
    translate = SelectField(
        'translate', validators=[DataRequired()],
        choices=[
            ('ar', 'ar'),
            ('de', 'de'),
            ('el', 'el'),
            ('es', 'es'),
            ('fa', 'fa'),
            ('hi', 'hi'),
            ('id', 'id'),
            ('it', 'it'),
            ('ka', 'ka'),
            ('mr', 'mr'),
            ('ms', 'ms'),
            ('pt', 'pt'),
            ('ro', 'ro'),
            ('ru', 'ks'),
            ('tk', 'tk'),
            ('tt', 'tt'),
            ('zh', 'zh'),
            ('zu', 'zu'),
        ]
    )