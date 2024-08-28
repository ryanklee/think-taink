import pytest
from src.ab_testing import ABTestRunner
from src.utils.metrics import calculate_sentiment_scores

@pytest.fixture
def ab_test_runner(tmp_path):
    config = {'principles': {'version_control_file': str(tmp_path / 'test_principles.json')}}
    return ABTestRunner(config)

def test_sentiment_analysis(ab_test_runner, mocker):
    # Mock input and results
    input_text = "What are your thoughts on artificial intelligence?"
    mock_results = {
        'openai': [
            [{'content': 'AI is fascinating and has great potential.'}],
            [{'content': 'AI raises important ethical considerations.'}]
        ],
        'anthropic': [
            [{'content': 'AI is a powerful tool that needs careful management.'}],
            [{'content': 'The future of AI looks promising but challenging.'}]
        ]
    }

    # Mock the run_ab_test method to return our mock results
    mocker.patch.object(ab_test_runner, 'run_ab_test', return_value=mock_results)

    # Mock the calculate_sentiment_scores function
    mocker.patch('src.utils.metrics.calculate_sentiment_scores', return_value=[0.5, -0.2])

    # Run the analysis
    analysis = ab_test_runner.analyze_results(mock_results)

    # Check if sentiment scores are calculated
    assert 'sentiment_scores' in analysis['openai']
    assert 'sentiment_scores' in analysis['anthropic']

    # Check if sentiment scores are within expected range (-1 to 1)
    for api in ['openai', 'anthropic']:
        scores = analysis[api]['sentiment_scores']
        assert all(-1 <= score <= 1 for score in scores)

    # Check if the number of sentiment scores matches the number of responses
    assert len(analysis['openai']['sentiment_scores']) == len(mock_results['openai'])
    assert len(analysis['anthropic']['sentiment_scores']) == len(mock_results['anthropic'])
