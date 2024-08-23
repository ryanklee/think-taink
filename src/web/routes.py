from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from src.web.forms import QuestionForm

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = QuestionForm()
    if form.validate_on_submit():
        question = form.question.data
        try:
            # Process the question and generate a response
            processed_input = current_app.input_processor.process(question)
            
            # Generate and process the response
            discussion = current_app.moderator.start_discussion(processed_input)
            
            # Generate the final output
            final_output = current_app.moderator.summarize_discussion(discussion)
            
            return render_template('result.html', question=question, response=final_output)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect(url_for('main.index'))
    return render_template('index.html', form=form)
