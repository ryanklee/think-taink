import pytest
from src.ab_testing import ABTestRunner
from src.utils.metrics import calculate_sentiment_scores

@pytest.fixture
def ab_test_runner(mocker):
    config = {'principles': {'version_control_file': 'test_principles.json'}}
    mocker.patch('src.llm_pool.llm_pool.LLMPool')
    mocker.patch('src.heuristics.principles.Principles')
    mocker.patch('src.moderator.moderator.Moderator')
    return ABTestRunner(config)

def test_sentiment_analysis(ab_test_runner):
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
    ab_test_runner.run_ab_test = lambda *args, **kwargs: mock_results

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
