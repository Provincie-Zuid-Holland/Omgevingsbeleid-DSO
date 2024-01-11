from abc import ABC, abstractmethod

from dso.builder.state_manager.state_manager import StateManager


class BuilderService(ABC):
    """
    Abstract base class for builder services.
    """

    @abstractmethod
    def apply(self, state_manager: StateManager) -> StateManager:
        """
        Applies the created builder service to the given state.

        Args:
            state_manager (StateManager): The state manager used to inject state.

        Returns:
            StateManager: The updated state manager.
        """
        pass
