from typing import List, Dict
from textblob import TextBlob

def calculate_response_metrics(api_results: List[Dict]) -> Dict:
    total_words = 0
    total_sentences = 0
    total_responses = 0

    for discussion in api_results:
        for response in discussion:
            text = response.get('content', '')
            blob = TextBlob(text)
            total_words += len(blob.words)
            total_sentences += len(blob.sentences)
            total_responses += 1

    return {
        'average_words_per_response': total_words / total_responses if total_responses > 0 else 0,
        'average_sentences_per_response': total_sentences / total_responses if total_responses > 0 else 0,
    }

def calculate_sentiment_scores(api_results: List[Dict]) -> Dict:
    total_polarity = 0
    total_subjectivity = 0
    total_responses = 0

    for discussion in api_results:
        for response in discussion:
            text = response.get('content', '')
            blob = TextBlob(text)
            total_polarity += blob.sentiment.polarity
            total_subjectivity += blob.sentiment.subjectivity
            total_responses += 1

    return {
        'average_polarity': total_polarity / total_responses if total_responses > 0 else 0,
        'average_subjectivity': total_subjectivity / total_responses if total_responses > 0 else 0,
    }
from typing import List, Dict
from textblob import TextBlob

def calculate_response_metrics(api_results: List[Dict]) -> Dict:
    # Implement response metrics calculation
    # This is a placeholder and should be implemented based on your specific requirements
    return {}

def calculate_sentiment_scores(api_results: List[Dict]) -> List[float]:
    sentiment_scores = []
    for result in api_results:
        discussion_sentiment = 0
        for message in result:
            content = message.get('content', '')
            blob = TextBlob(content)
            discussion_sentiment += blob.sentiment.polarity
        average_sentiment = discussion_sentiment / len(result) if result else 0
        sentiment_scores.append(average_sentiment)
    return sentiment_scores
