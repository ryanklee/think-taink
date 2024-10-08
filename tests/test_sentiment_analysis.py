import pytest
import logging
import nltk
from src.ab_testing import ABTestRunner
from src.utils.metrics import calculate_sentiment_scores

@pytest.fixture(scope="session", autouse=True)
def download_nltk_data():
    nltk.download('punkt')

@pytest.fixture
def ab_test_runner(tmp_path):
    config = {'principles': {'version_control_file': str(tmp_path / 'test_principles.json')}}
    return ABTestRunner(config)

def test_sentiment_analysis(ab_test_runner, mocker, caplog):
    caplog.set_level(logging.DEBUG)
    
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
    mocker.patch('src.utils.metrics.calculate_sentiment_scores', return_value=[0.5, 0.5])

    # Mock the calculate_response_metrics function
    mocker.patch('src.utils.metrics.calculate_response_metrics', return_value={})

    # Mock TextBlob and NLTK to avoid data issues
    mocker.patch('nltk.tokenize.sent_tokenize', return_value=['AI is fascinating and has great potential.'])
    mocker.patch('nltk.tokenize.word_tokenize', return_value=['AI', 'is', 'fascinating', 'and', 'has', 'great', 'potential'])
    mocker.patch('textblob.TextBlob.sentiment', new_callable=mocker.PropertyMock, return_value=mocker.Mock(polarity=0.5, subjectivity=0.5))
    mocker.patch('textblob.TextBlob.sentences', new_callable=mocker.PropertyMock, return_value=[mocker.Mock(raw='AI is fascinating and has great potential.')])

    # Run the analysis
    analysis = ab_test_runner.analyze_results(mock_results)

    # Check if sentiment scores are calculated
    assert 'sentiment_scores' in analysis['openai']
    assert 'sentiment_scores' in analysis['anthropic']

    # Check if sentiment scores are present and match the mocked values
    assert analysis['openai']['sentiment_scores'] == [0.5, 0.5]
    assert analysis['anthropic']['sentiment_scores'] == [0.5, 0.5]

    # Check if the number of sentiment scores matches the number of responses
    assert len(analysis['openai']['sentiment_scores']) == 2
    assert len(analysis['anthropic']['sentiment_scores']) == 2

    # Check if the expected log messages are present
    assert "Starting result analysis" in caplog.text
    assert "Analyzing results for OpenAI" in caplog.text
    assert "Analyzing results for Claude" in caplog.text
    assert "Analysis completed for OpenAI" in caplog.text
    assert "Analysis completed for Claude" in caplog.text
    assert "Starting comparison of OpenAI and Claude results" in caplog.text
    assert "Comparison of OpenAI and Claude results completed" in caplog.text
    assert "Result analysis completed" in caplog.text

    # Print out all captured logs for debugging
    print("\nCaptured logs:")
    print(caplog.text)

    # Test hypotheses ranking
    ranked_hypotheses = ab_test_runner.rank_hypotheses(mock_results)
    assert len(ranked_hypotheses) == 4
    assert all('api' in h and 'iteration' in h and 'hypothesis' in h and 'score' in h for h in ranked_hypotheses)
