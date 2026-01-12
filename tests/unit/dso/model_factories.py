from enum import IntEnum
from typing import Optional

from dso.models import GioFRBR, PubdataFRBR, InstellingDoel, DoelFRBR, ActFRBR
from tests.factory import Factory


class FRBRType(IntEnum):
    GEBIED = 100
    DOCUMENT = 200
    ACT = 300
    PUB_DATA = 400


class GioFRBRFactory(Factory):
    Work_Province_ID: str = "pv28"
    Work_Other: str = "omgevingsvisie-1"
    Expression_Language: str = "nld"
    Work_Date: str = "2025"
    Expression_Date: str = "2025-11-25"
    Expression_Version: int
    frbr_type: FRBRType

    def create(self) -> GioFRBR:
        return GioFRBR(
            Work_Province_ID=self.Work_Province_ID,
            Work_Other=self.Work_Other,
            Expression_Language=self.Expression_Language,
            Work_Date=self.Work_Date,
            Expression_Date=self.Expression_Date,
            Expression_Version=self.frbr_type + self.Expression_Version,
        )


class PubdataFRBRFactory(Factory):
    Work_Province_ID: str = "pv28"
    Work_Other: str = "omgevingsvisie-1"
    Expression_Language: str = "nld"
    Work_Date: str = "2025"
    Expression_Date: str = "2025-11-25"
    Expression_Version: int

    def create(self) -> PubdataFRBR:
        return PubdataFRBR(
            Work_Province_ID=self.Work_Province_ID,
            Work_Other=self.Work_Other,
            Expression_Language=self.Expression_Language,
            Work_Date=self.Work_Date,
            Expression_Date=self.Expression_Date,
            Expression_Version=FRBRType.PUB_DATA + self.Expression_Version,
        )


class DoelFRBRFactory(Factory):
    Work_Province_ID: str = "pv28"
    Work_Other: str = "omgevingsvisie-1"
    Work_Date: str = "2025"

    def create(self) -> DoelFRBR:
        return DoelFRBR(
            Work_Province_ID=self.Work_Province_ID,
            Work_Other=self.Work_Other,
            Work_Date=self.Work_Date,
        )


class ActFRBRFactory(Factory):
    Work_Country: str = "nl"
    Work_Province_ID: str = "pv28"
    Work_Other: str = "omgevingsvisie-1"
    Expression_Language: str = "nld"
    Work_Date: str = "2025"
    Expression_Date: str = "2025-11-25"
    Expression_Version: int

    def create(self) -> ActFRBR:
        return ActFRBR(
            Work_Country=self.Work_Country,
            Work_Province_ID=self.Work_Province_ID,
            Work_Other=self.Work_Other,
            Expression_Language=self.Expression_Language,
            Work_Date=self.Work_Date,
            Expression_Date=self.Expression_Date,
            Expression_Version=FRBRType.ACT + self.Expression_Version,
        )


class InstellingDoelFactory(Factory):
    datum_juridisch_werkend_vanaf: Optional[str] = None

    def create(self) -> InstellingDoel:
        return InstellingDoel(
            frbr=DoelFRBRFactory().create(),
            datum_juridisch_werkend_vanaf=self.datum_juridisch_werkend_vanaf,
        )
