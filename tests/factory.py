import uuid
from abc import ABC, abstractmethod
from enum import Enum

from pydantic import BaseModel


class TypeEnum(Enum):
    GEBIED = 1
    DOCUMENT = 2
    BESLUIT_PDF = 3


class Factory(ABC, BaseModel):
    @abstractmethod
    def create(self) -> BaseModel:
        pass

    @staticmethod
    def get_uuid_from_id(the_type: TypeEnum, the_id: int) -> uuid.UUID:
        return uuid.UUID(f"00000000-0000-0000-{str(the_type.value).zfill(4)}-{str(the_id).zfill(12)}")
