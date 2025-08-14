from abc import ABC, abstractmethod


class AbstractEnricher(ABC):
    @abstractmethod
    def enrich_xml(self, xml_content: str) -> str:
        pass
