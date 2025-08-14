from abc import ABC, abstractmethod

from .state_manager.state_manager import StateManager


class BuilderService(ABC):
    @abstractmethod
    def apply(self, state_manager: StateManager) -> StateManager:
        pass
