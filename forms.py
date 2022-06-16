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
            ('ha', 'ha'),
            ('hi', 'hi'),
            ('id', 'id'),
            ('ig', 'ig'),
            ('it', 'it'),
            ('ka', 'ka'),
            ('mr', 'mr'),
            ('ms', 'ms'),
            ('nso', 'nso'),
            ('pt', 'pt'),
            ('ro', 'ro'),
            ('ru', 'ks'),
            ('tg', 'tg'),
            ('tk', 'tk'),
            ('tn', 'tn'),
            ('tpi', 'tpi'),
            ('tt', 'tt'),
            ('xh', 'xh'),
            ('yo', 'yo'),
            ('zh', 'zh'),
            ('zu', 'zu'),
        ]
    )