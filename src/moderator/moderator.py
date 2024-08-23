from typing import List, Dict
from src.llm_pool.llm_pool import LLMPool
from src.heuristics.principles import Principles
from src.principles_evolution.reflector import Reflector
from src.llm_pool.pool_evolution import PoolEvolution

class Moderator:
    def __init__(self, llm_pool: LLMPool, principles: Principles):
        self.llm_pool = llm_pool
        self.principles = principles
        self.reflector = Reflector(principles, llm_pool)
        self.pool_evolution = PoolEvolution(llm_pool)
        self.max_turns = 10
        self.current_turn = 0

    def start_discussion(self, input_text: str) -> List[Dict]:
        discussion = []
        try:
            while self.current_turn < self.max_turns:
                for expert in self.llm_pool.get_expert_names():
                    expert_prompt = self.llm_pool.get_expert_prompt(expert)
                    response = self.llm_pool.generate_response(f"{expert_prompt}\n\nQuestion: {input_text}")
                    evaluated_response = self.principles.evaluate_response(response[0]['response'])
                    discussion.append({"expert": expert, "response": evaluated_response})
                    self.current_turn += 1
                    if self.current_turn >= self.max_turns:
                        break
                input_text = self._summarize_current_discussion(discussion)
            
            # Reflect on principles after the discussion
            self._reflect_on_principles(discussion)
            
            # Evolve the expert pool after the discussion
            self._evolve_expert_pool(discussion)
        except Exception as e:
            raise ModerationError(f"Error in start_discussion: {str(e)}")
        
        return discussion

    def summarize_discussion(self, discussion: List[Dict]) -> str:
        summary_prompt = "Summarize the following discussion points into a coherent response:\n\n"
        for entry in discussion:
            summary_prompt += f"{entry['expert']}: {entry['response']}\n\n"
        summary_prompt += "Final summary:"
        summary = self.llm_pool.generate_response(summary_prompt)[0]['response']
        return summary

    def _summarize_current_discussion(self, discussion: List[Dict]) -> str:
        summary_prompt = "Summarize the following discussion points concisely:"
        for entry in discussion[-len(self.llm_pool.get_expert_names()):]:
            summary_prompt += f"\n{entry['expert']}: {entry['response']}"
        return self.llm_pool.generate_response(summary_prompt)[0]['response']

    def intervene(self, discussion: List[Dict]) -> str:
        intervention_prompt = "As a moderator, provide guidance to keep the discussion on track and productive based on the following discussion points:"
        for entry in discussion[-3:]:  # Consider the last 3 entries
            intervention_prompt += f"\n{entry['expert']}: {entry['response']}"
        return self.llm_pool.generate_response(intervention_prompt)

    def _reflect_on_principles(self, discussion: List[Dict]):
        suggestions = self.reflector.reflect_on_principles(discussion)
        self.principles.apply_reflector_suggestions(suggestions)

    def _evolve_expert_pool(self, discussion: List[Dict]):
        self.pool_evolution.evolve_pool(discussion)
