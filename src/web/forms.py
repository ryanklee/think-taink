from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    question = StringField('Enter your question:', validators=[DataRequired()])
    api_type = SelectField('Select API:', choices=[('openai', 'OpenAI'), ('anthropic', 'Claude')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class ImprovementForm(FlaskForm):
    submit = SubmitField('Run Improvement Cycle')
