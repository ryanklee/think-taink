from flask import Blueprint, render_template, flash, redirect, url_for, current_app, Response, stream_with_context, request, jsonify
from src.web.forms import QuestionForm, ImprovementForm
from src.web.models import db, Question
import json

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/ask', methods=['GET', 'POST'])
def ask_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = form.question.data
        api_type = form.api_type.data
        # Save the question to the database
        new_question = Question(text=question, api_type=api_type)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('main.result', question=question, api_type=api_type))
    
    # Fetch recent questions
    recent_questions = Question.query.order_by(Question.created_at.desc()).limit(5).all()
    
    return render_template('ask_question.html', form=form, recent_questions=recent_questions)

@bp.route('/result')
def result():
    question = request.args.get('question')
    api_type = request.args.get('api_type')
    return render_template('result.html', question=question, api_type=api_type)

import logging

logger = logging.getLogger(__name__)

@bp.route('/stream', methods=['GET', 'POST'])
def stream_response():
    question = request.args.get('question') or request.form.get('question')
    api_type = request.args.get('api_type') or request.form.get('api_type') or 'openai'  # Default to 'openai' if not specified
    logger.info(f"Received stream request for question: {question}, API type: {api_type}")
    try:
        processed_input = current_app.input_processor.process(question)
        
        # Check if llm_pools exists in current_app
        if not hasattr(current_app, 'llm_pools'):
            logger.error("llm_pools not found in current_app")
            return jsonify({"error": "LLM pools not configured"}), 500
        
        # Set the API type for the moderator
        if api_type not in current_app.llm_pools:
            logger.error(f"Invalid API type: {api_type}, defaulting to 'openai'")
            api_type = 'openai'
        
        current_app.moderator.set_llm_pool(current_app.llm_pools[api_type])
        
        def generate():
            try:
                for chunk in current_app.moderator.start_discussion_stream(processed_input):
                    response_text = chunk['response']
                    if isinstance(response_text, dict):
                        response_text = json.dumps(response_text)
                    else:
                        response_text = str(response_text)
                    yield f"data: {json.dumps({'expert': chunk['expert'], 'response': response_text})}\n\n"
            except Exception as e:
                logger.error(f"Error in stream generation: {str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        return Response(stream_with_context(generate()), mimetype='text/event-stream')
    except Exception as e:
        logger.error(f"Error in stream_response: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/dashboard')
def improvement_dashboard():
    form = ImprovementForm()
    
    # Mock data for performance metrics (replace with actual data in the future)
    metrics = {
        'Average Response Time': '2.5 seconds',
        'Discussion Quality Score': '8.7/10',
        'Principle Evolution Rate': '0.05 per discussion'
    }
    
    # Get the current configuration
    config = current_app.config
    
    return render_template('improvement_dashboard.html', form=form, metrics=metrics, config=config)

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
