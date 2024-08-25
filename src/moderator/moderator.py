from typing import List, Dict, Generator
import logging
from src.llm_pool.llm_pool import LLMPool
from src.heuristics.principles import Principles
from src.principles_evolution.reflector import Reflector
from src.llm_pool.pool_evolution import PoolEvolution
from src.utils.exceptions import ModerationError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Moderator:
    def __init__(self, llm_pool: LLMPool, principles: Principles):
        logger.debug("Initializing Moderator")
        self.llm_pool = llm_pool
        self.principles = principles
        self.reflector = Reflector(principles, llm_pool)
        self.pool_evolution = PoolEvolution(llm_pool)
        self.max_turns = 10
        self.current_turn = 0
        logger.debug(f"Moderator initialized with max_turns: {self.max_turns}")

    def start_discussion_stream(self, input_text: str) -> Generator[Dict[str, str], None, None]:
        logger.debug(f"Starting discussion stream for input: {input_text[:50]}...")
        try:
            while self.current_turn < self.max_turns:
                logger.debug(f"Starting turn {self.current_turn + 1}")
                for expert in self.llm_pool.get_expert_names():
                    expert_prompt = self.llm_pool.get_expert_prompt(expert)
                    try:
                        logger.debug(f"Generating response for expert: {expert}")
                        response_stream = self.llm_pool.generate_response_stream(f"{expert_prompt}\n\nQuestion: {input_text}")
                        for response_chunk in response_stream:
                            logger.debug(f"Received response chunk for {expert}: {response_chunk}")
                            evaluated_chunk = self.principles.evaluate_response(response_chunk['response'])
                            logger.debug(f"Evaluated response chunk for {expert}: {evaluated_chunk}")
                            yield {"expert": expert, "response": evaluated_chunk}
                        self.current_turn += 1
                        logger.debug(f"Completed turn {self.current_turn}")
                        if self.current_turn >= self.max_turns:
                            logger.debug("Reached max turns, breaking out of expert loop")
                            break
                    except Exception as e:
                        logger.error(f"Error generating response for {expert}: {str(e)}")
                        yield {"expert": expert, "response": f"Error: {str(e)}"}
                if self.current_turn >= self.max_turns:
                    logger.debug("Reached max turns, breaking out of main loop")
                    break
                try:
                    logger.debug("Getting last turn")
                    last_turn = list(self._get_last_turn())
                    logger.debug(f"Last turn: {last_turn}")
                    logger.debug("Summarizing current discussion")
                    input_text = self._summarize_current_discussion(last_turn)
                    logger.debug(f"Summarized discussion: {input_text}")
                except Exception as e:
                    logger.error(f"Error summarizing discussion: {str(e)}")
                    yield {"expert": "System", "response": f"Error summarizing discussion: {str(e)}"}
            
            # Reflect on principles after the discussion
            try:
                logger.debug("Reflecting on principles")
                yield from self._reflect_on_principles_stream()
            except Exception as e:
                logger.error(f"Error reflecting on principles: {str(e)}")
                yield {"expert": "System", "response": f"Error reflecting on principles: {str(e)}"}
            
            # Evolve the expert pool after the discussion
            try:
                logger.debug("Evolving expert pool")
                yield from self._evolve_expert_pool_stream()
            except Exception as e:
                logger.error(f"Error evolving expert pool: {str(e)}")
                yield {"expert": "System", "response": f"Error evolving expert pool: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error in start_discussion_stream: {str(e)}")
            yield {"expert": "System", "response": f"Unexpected error: {str(e)}"}
        logger.debug("Finished discussion stream")

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
