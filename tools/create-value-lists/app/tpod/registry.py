from abc import ABC, abstractmethod

from .source_models import SourceResult


class WaardelijstProcessor(ABC):
    @abstractmethod
    def process(self, source: SourceResult) -> str:
        pass


class WaardelijstProcessorRegistry:
    def __init__(self):
        self._registry: dict[str, WaardelijstProcessor] = {}

    def add(self, key: str, processor: WaardelijstProcessor):
        self._registry[key] = processor

    def get_all(self) -> dict[str, WaardelijstProcessor]:
        return self._registry
