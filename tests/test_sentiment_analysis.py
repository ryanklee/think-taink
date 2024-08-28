import pytest
import logging
from src.ab_testing import ABTestRunner
from src.utils.metrics import calculate_sentiment_scores

@pytest.fixture
def ab_test_runner(tmp_path):
    config = {'principles': {'version_control_file': str(tmp_path / 'test_principles.json')}}
    return ABTestRunner(config)

def test_sentiment_analysis(ab_test_runner, mocker):
    # Mock the logger
    mock_logger = mocker.Mock(spec=logging.Logger)
    mocker.patch.object(ab_test_runner, 'logger', mock_logger)

    # Mock input and results
    input_text = "What are your thoughts on artificial intelligence?"
    mock_results = {
        'openai': [
            [{'content': 'AI is fascinating and has great potential.', 'hypothesis': 'AI has great potential'}],
            [{'content': 'AI raises important ethical considerations.', 'hypothesis': 'AI raises ethical concerns'}]
        ],
        'anthropic': [
            [{'content': 'AI is a powerful tool that needs careful management.', 'hypothesis': 'AI needs careful management'}],
            [{'content': 'The future of AI looks promising but challenging.', 'hypothesis': 'AI future is promising and challenging'}]
        ]
    }

    # Mock the run_ab_test method to return our mock results
    mocker.patch.object(ab_test_runner, 'run_ab_test', return_value=mock_results)

    # Mock the calculate_sentiment_scores function
    mocker.patch('src.utils.metrics.calculate_sentiment_scores', return_value=[0.5, -0.2])

    # Mock the calculate_response_metrics function
    mocker.patch('src.utils.metrics.calculate_response_metrics', return_value={})

    # Run the analysis
    analysis = ab_test_runner.analyze_results(mock_results)

    # Check if sentiment scores are calculated
    assert 'sentiment_scores' in analysis['openai']
    assert 'sentiment_scores' in analysis['anthropic']

    # Check if sentiment scores are present and match the mocked values
    assert analysis['openai']['sentiment_scores'] == [0.5, -0.2]
    assert analysis['anthropic']['sentiment_scores'] == [0.5, -0.2]

    # Check if the number of sentiment scores matches the number of responses
    assert len(analysis['openai']['sentiment_scores']) == 2
    assert len(analysis['anthropic']['sentiment_scores']) == 2

    # Check if the logger.info was called for the analysis
    mock_logger.info.assert_any_call("Result analysis completed")
    mock_logger.info.assert_any_call("Comparison of OpenAI and Claude results completed")

    # Test hypotheses ranking
    ranked_hypotheses = ab_test_runner.rank_hypotheses(mock_results)
    assert len(ranked_hypotheses) == 4
    assert all('api' in h and 'iteration' in h and 'hypothesis' in h and 'score' in h for h in ranked_hypotheses)
