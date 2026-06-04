from abc import ABC, abstractmethod
from typing import Dict

from .source_models import SourceResult


class WaardelijstProcessor(ABC):
    @abstractmethod
    def process(self, source: SourceResult) -> str:
        pass


class WaardelijstProcessorRegistry:
    def __init__(self):
        self._registry: Dict[str, WaardelijstProcessor] = {}

    def add(self, key: str, processor: WaardelijstProcessor):
        self._registry[key] = processor

    def get_all(self) -> Dict[str, WaardelijstProcessor]:
        return self._registry
