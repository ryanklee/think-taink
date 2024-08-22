from typing import List, Dict
from src.llm_pool.llm_pool import LLMPool

class Moderator:
    def __init__(self, llm_pool: LLMPool):
        self.llm_pool = llm_pool
        self.max_turns = 10
        self.current_turn = 0

    def start_discussion(self, input_text: str) -> List[Dict]:
        discussion = []
        while self.current_turn < self.max_turns:
            for expert in self.llm_pool.get_expert_names():
                response = self.llm_pool.generate_response(input_text)
                discussion.append({"expert": expert, "response": response})
                self.current_turn += 1
                if self.current_turn >= self.max_turns:
                    break
            input_text = self._summarize_current_discussion(discussion)
        return discussion

    def _summarize_current_discussion(self, discussion: List[Dict]) -> str:
        # TODO: Implement a more sophisticated summarization method
        return " ".join([d["response"] for d in discussion[-len(self.llm_pool.get_expert_names()):]])
