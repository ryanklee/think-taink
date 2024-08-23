from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    question = StringField('Enter your question:', validators=[DataRequired()])
    submit = SubmitField('Submit')
