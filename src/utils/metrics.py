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
import logging

logger = logging.getLogger(__name__)

def calculate_response_metrics(api_results: List[Dict]) -> Dict:
    total_words = 0
    total_sentences = 0
    total_messages = 0

    for result in api_results:
        for message in result:
            content = message.get('content', '')
            blob = TextBlob(content)
            total_words += len(blob.words)
            total_sentences += len(blob.sentences)
            total_messages += 1

    avg_words_per_message = total_words / total_messages if total_messages > 0 else 0
    avg_sentences_per_message = total_sentences / total_messages if total_messages > 0 else 0

    return {
        'avg_words_per_message': avg_words_per_message,
        'avg_sentences_per_message': avg_sentences_per_message,
        'total_messages': total_messages
    }

def calculate_sentiment_scores(api_results: List[Dict]) -> List[float]:
    sentiment_scores = []
    for result in api_results:
        discussion_sentiment = 0
        message_count = 0
        for message in result:
            try:
                content = message.get('content', '')
                blob = TextBlob(content)
                discussion_sentiment += blob.sentiment.polarity
                message_count += 1
            except Exception as e:
                logger.error(f"Error calculating sentiment for message: {str(e)}")
        
        average_sentiment = discussion_sentiment / message_count if message_count > 0 else 0
        sentiment_scores.append(average_sentiment)
    
    logger.info(f"Calculated sentiment scores: {sentiment_scores}")
    return sentiment_scores
