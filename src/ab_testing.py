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
        # Implement your analysis logic here
        # This is a placeholder implementation
        total_responses = sum(len(result) for result in api_results)
        avg_responses = total_responses / len(api_results)
        return {
            'average_responses_per_discussion': avg_responses,
            'total_discussions': len(api_results)
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
