from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from src.web.forms import QuestionForm, ImprovementForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/ask', methods=['GET', 'POST'])
def ask_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = form.question.data
        try:
            processed_input = current_app.input_processor.process(question)
            discussion = current_app.moderator.start_discussion(processed_input)
            final_output = current_app.moderator.summarize_discussion(discussion)
            return render_template('result.html', question=question, response=final_output)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect(url_for('main.ask_question'))
    return render_template('ask_question.html', form=form)

@bp.route('/dashboard')
def improvement_dashboard():
    form = ImprovementForm()
    return render_template('improvement_dashboard.html', form=form)

@bp.route('/run_improvement', methods=['POST'])
def run_improvement():
    form = ImprovementForm()
    if form.validate_on_submit():
        try:
            # Implement the improvement run logic here
            flash("Improvement run completed successfully", 'success')
        except Exception as e:
            flash(f"An error occurred during the improvement run: {str(e)}", 'error')
    return redirect(url_for('main.improvement_dashboard'))
