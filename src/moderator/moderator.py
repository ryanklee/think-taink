from typing import List, Dict, Generator
import logging
from src.llm_pool.llm_pool import LLMPool
from src.heuristics.principles import Principles
from src.principles_evolution.reflector import Reflector
from src.llm_pool.pool_evolution import PoolEvolution
from src.utils.exceptions import ModerationError

class Moderator:
    def __init__(self, llm_pool: LLMPool, principles: Principles):
        self.llm_pool = llm_pool
        self.principles = principles
        self.reflector = Reflector(principles, llm_pool)
        self.pool_evolution = PoolEvolution(llm_pool)
        self.max_turns = 10
        self.current_turn = 0

    def start_discussion_stream(self, input_text: str) -> Generator[Dict[str, str], None, None]:
        try:
            while self.current_turn < self.max_turns:
                for expert in self.llm_pool.get_expert_names():
                    expert_prompt = self.llm_pool.get_expert_prompt(expert)
                    try:
                        for response_chunk in self.llm_pool.generate_response_stream(f"{expert_prompt}\n\nQuestion: {input_text}"):
                            evaluated_chunk = self.principles.evaluate_response(response_chunk['response'])
                            yield {"expert": expert, "response": evaluated_chunk}
                        self.current_turn += 1
                        if self.current_turn >= self.max_turns:
                            break
                    except Exception as e:
                        logging.error(f"Error generating response for {expert}: {str(e)}")
                        yield {"expert": expert, "response": f"Error: {str(e)}"}
                if self.current_turn >= self.max_turns:
                    break
                try:
                    last_turn = list(self._get_last_turn())
                    input_text = self._summarize_current_discussion(last_turn)
                except Exception as e:
                    logging.error(f"Error summarizing discussion: {str(e)}")
                    yield {"expert": "System", "response": f"Error summarizing discussion: {str(e)}"}
            
            # Reflect on principles after the discussion
            try:
                yield from self._reflect_on_principles_stream()
            except Exception as e:
                logging.error(f"Error reflecting on principles: {str(e)}")
                yield {"expert": "System", "response": f"Error reflecting on principles: {str(e)}"}
            
            # Evolve the expert pool after the discussion
            try:
                yield from self._evolve_expert_pool_stream()
            except Exception as e:
                logging.error(f"Error evolving expert pool: {str(e)}")
                yield {"expert": "System", "response": f"Error evolving expert pool: {str(e)}"}
        except Exception as e:
            logging.error(f"Unexpected error in start_discussion_stream: {str(e)}")
            yield {"expert": "System", "response": f"Unexpected error: {str(e)}"}

    def _get_last_turn(self) -> Generator[Dict[str, str], None, None]:
        for expert in self.llm_pool.get_expert_names():
            yield {"expert": expert, "response": "Last response for this expert"}

    def _reflect_on_principles_stream(self) -> Generator[Dict[str, str], None, None]:
        yield {"expert": "System", "response": "Reflecting on principles..."}
        # Implement the streaming version of reflection here

    def _evolve_expert_pool_stream(self) -> Generator[Dict[str, str], None, None]:
        yield {"expert": "System", "response": "Evolving expert pool..."}
        # Implement the streaming version of expert pool evolution here

    def summarize_discussion(self, discussion: List[Dict]) -> str:
        summary_prompt = "Summarize the following discussion points into a coherent response:\n\n"
        for entry in discussion:
            summary_prompt += f"{entry['expert']}: {entry['response']}\n\n"
        summary_prompt += "Final summary:"
        summary = next(self.llm_pool.generate_response_stream(summary_prompt))['response']
        return summary

    def _summarize_current_discussion(self, discussion: List[Dict]) -> str:
        summary_prompt = "Summarize the following discussion points concisely:"
        for entry in discussion[-len(self.llm_pool.get_expert_names()):]:
            summary_prompt += f"\n{entry['expert']}: {entry['response']}"
        return next(self.llm_pool.generate_response_stream(summary_prompt))['response']

    def intervene(self, discussion: List[Dict]) -> str:
        intervention_prompt = "As a moderator, provide guidance to keep the discussion on track and productive based on the following discussion points:"
        for entry in discussion[-3:]:  # Consider the last 3 entries
            intervention_prompt += f"\n{entry['expert']}: {entry['response']}"
        return next(self.llm_pool.generate_response_stream(intervention_prompt))['response']

    def _reflect_on_principles(self, discussion: List[Dict]):
        suggestions = self.reflector.reflect_on_principles(discussion)
        self.principles.apply_reflector_suggestions(suggestions)

    def _evolve_expert_pool(self, discussion: List[Dict]):
        self.pool_evolution.evolve_pool(discussion)
