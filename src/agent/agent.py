from abc import ABC, abstractmethod
from typing import Dict, Any

class Agent(ABC):
    """
    Abstract base class for all agents in the Collaborative AI Reasoning System.
    """

    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return a response.

        Args:
            input_data (Dict[str, Any]): The input data for the agent to process.

        Returns:
            Dict[str, Any]: The processed output from the agent.
        """
        pass

    @abstractmethod
    def update_knowledge(self, new_knowledge: Dict[str, Any]) -> None:
        """
        Update the agent's knowledge base.

        Args:
            new_knowledge (Dict[str, Any]): New knowledge to be added or updated.
        """
        pass

    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the agent.

        Returns:
            Dict[str, Any]: The current state of the agent.
        """
        pass

    @abstractmethod
    def set_state(self, state: Dict[str, Any]) -> None:
        """
        Set the state of the agent.

        Args:
            state (Dict[str, Any]): The state to set for the agent.
        """
        pass
