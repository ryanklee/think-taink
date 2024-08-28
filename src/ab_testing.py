import random
import logging
import os
from typing import List, Dict
from src.llm_pool.llm_pool import LLMPool
from src.moderator.moderator import Moderator
from src.heuristics.principles import Principles
from src.utils.metrics import calculate_response_metrics, calculate_sentiment_scores

class ABTestRunner:
    def __init__(self, config: Dict):
        self.config = config
        self.openai_llm_pool = LLMPool(config, api_type='openai')
        self.claude_llm_pool = LLMPool(config, api_type='anthropic')
        self.principles = Principles(config['principles']['version_control_file'])
        self.openai_moderator = Moderator(self.openai_llm_pool, self.principles)
        self.claude_moderator = Moderator(self.claude_llm_pool, self.principles)
        self.logger = logging.getLogger(__name__)

        # Log API key status
        self.logger.info(f"OpenAI API key status: {'Set' if os.environ.get('OPENAI_API_KEY') else 'Not set'}")
        self.logger.info(f"Anthropic API key status: {'Set' if os.environ.get('ANTHROPIC_API_KEY') else 'Not set'}")

    def run_ab_test(self, input_text: str, num_iterations: int = 5) -> Dict[str, List[Dict]]:
        results = {
            'openai': [],
            'anthropic': []
        }

        self.logger.info(f"Starting AB test with input: {input_text}")
        for i in range(num_iterations):
            self.logger.info(f"Starting iteration {i+1} of {num_iterations}")
            
            # Run OpenAI test
            self.logger.debug(f"Running OpenAI test for iteration {i+1}")
            try:
                openai_result = list(self.openai_moderator.start_discussion_stream(input_text))
                results['openai'].append(openai_result)
                self.logger.info(f"OpenAI test completed for iteration {i+1}")
            except Exception as e:
                self.logger.error(f"Error in OpenAI test for iteration {i+1}: {str(e)}")
                results['openai'].append([])

            # Run Claude test
            self.logger.debug(f"Running Claude test for iteration {i+1}")
            try:
                claude_result = list(self.claude_moderator.start_discussion_stream(input_text))
                results['anthropic'].append(claude_result)
                self.logger.info(f"Claude test completed for iteration {i+1}")
            except Exception as e:
                self.logger.error(f"Error in Claude test for iteration {i+1}: {str(e)}")
                results['anthropic'].append([])

        self.logger.info("AB test completed")
        return results

    def analyze_results(self, results: Dict[str, List[Dict]]) -> Dict[str, Dict]:
        self.logger.info("Starting result analysis")
        analysis = {
            'openai': self._analyze_api_results(results['openai'], 'OpenAI'),
            'anthropic': self._analyze_api_results(results['anthropic'], 'Claude')
        }
        
        # Compare the results
        comparison = self._compare_results(analysis['openai'], analysis['anthropic'])
        analysis['comparison'] = comparison

        self.logger.info("Result analysis completed")
        return analysis

    def _analyze_api_results(self, api_results: List[Dict], api_name: str) -> Dict:
        self.logger.debug(f"Analyzing results for {api_name}")
        total_responses = sum(len(result) for result in api_results if result)
        avg_responses = total_responses / len(api_results) if api_results else 0
        
        response_metrics = calculate_response_metrics(api_results)
        sentiment_scores = calculate_sentiment_scores(api_results)
        
        analysis = {
            'average_responses_per_discussion': avg_responses,
            'total_discussions': len(api_results),
            'response_metrics': response_metrics,
            'sentiment_scores': sentiment_scores
        }
        
        self.logger.info(f"Analysis completed for {api_name}")
        return analysis

    def _compare_results(self, openai_analysis: Dict, claude_analysis: Dict) -> Dict:
        self.logger.debug("Starting comparison of OpenAI and Claude results")
        comparison = {}
        
        for metric in openai_analysis.keys():
            if isinstance(openai_analysis[metric], (int, float)) and isinstance(claude_analysis[metric], (int, float)):
                difference = openai_analysis[metric] - claude_analysis[metric]
                percentage_difference = (difference / openai_analysis[metric]) * 100 if openai_analysis[metric] != 0 else 0
                comparison[metric] = {
                    'difference': difference,
                    'percentage_difference': percentage_difference
                }
            elif metric == 'sentiment_scores':
                openai_avg = sum(openai_analysis[metric]) / len(openai_analysis[metric]) if openai_analysis[metric] else 0
                claude_avg = sum(claude_analysis[metric]) / len(claude_analysis[metric]) if claude_analysis[metric] else 0
                difference = openai_avg - claude_avg
                percentage_difference = (difference / openai_avg) * 100 if openai_avg != 0 else 0
                comparison[metric] = {
                    'difference': difference,
                    'percentage_difference': percentage_difference
                }
        
        self.logger.info("Comparison of OpenAI and Claude results completed")
        return comparison

    def run_ab_test(self, input_text: str, num_iterations: int = 5) -> Dict[str, List[Dict]]:
        results = {
            'openai': [],
            'anthropic': []
        }

        for _ in range(num_iterations):
            # Run OpenAI test
            openai_result = list(self.openai_moderator.start_discussion_stream(input_text))
            results['openai'].append(openai_result)

            # Run Claude test
            claude_result = list(self.claude_moderator.start_discussion_stream(input_text))
            results['anthropic'].append(claude_result)

        return results

    def analyze_results(self, results: Dict[str, List[Dict]]) -> Dict[str, Dict]:
        analysis = {
            'openai': self._analyze_api_results(results['openai']),
            'anthropic': self._analyze_api_results(results['anthropic'])
        }
        
        # Compare the results
        comparison = self._compare_results(analysis['openai'], analysis['anthropic'])
        analysis['comparison'] = comparison

        return analysis

    def _analyze_api_results(self, api_results: List[Dict]) -> Dict:
        total_responses = sum(len(result) for result in api_results)
        avg_responses = total_responses / len(api_results)
        
        # Calculate sentiment scores
        all_responses = [response['content'] for result in api_results for response in result]
        sentiment_scores = calculate_sentiment_scores(all_responses)
        
        # Calculate response metrics
        response_metrics = calculate_response_metrics(api_results)
        
        return {
            'average_responses_per_discussion': avg_responses,
            'total_discussions': len(api_results),
            'sentiment_scores': sentiment_scores,
            **response_metrics
        }
    def _compare_results(self, openai_analysis: Dict, claude_analysis: Dict) -> Dict:
        comparison = {}
        
        for metric in openai_analysis.keys():
            if isinstance(openai_analysis[metric], (int, float)):
                difference = openai_analysis[metric] - claude_analysis[metric]
                percentage_difference = (difference / openai_analysis[metric]) * 100
                comparison[metric] = {
                    'difference': difference,
                    'percentage_difference': percentage_difference
                }
            elif metric == 'sentiment_scores':
                openai_avg = sum(openai_analysis[metric]) / len(openai_analysis[metric])
                claude_avg = sum(claude_analysis[metric]) / len(claude_analysis[metric])
                difference = openai_avg - claude_avg
                percentage_difference = (difference / openai_avg) * 100 if openai_avg != 0 else 0
                comparison[metric] = {
                    'difference': difference,
                    'percentage_difference': percentage_difference
                }
        
        self.logger.info("Comparison of OpenAI and Claude results completed")
        return comparison
