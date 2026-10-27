from enum import IntEnum

from dso.models import ActFRBR, DoelFRBR, GioFRBR, InstellingDoel, PubdataFRBR
from tests.factory import Factory


class FRBRType(IntEnum):
    GEBIED = 100
    DOCUMENT = 200
    ACT = 300
    PUB_DATA = 400


class GioFRBRFactory(Factory):
    work_province_id: str = "pv28"
    work_other: str = "omgevingsvisie-1"
    expression_language: str = "nld"
    work_date: str = "2025"
    expression_date: str = "2025-11-25"
    expression_version: int
    frbr_type: FRBRType

    def create(self) -> GioFRBR:
        return GioFRBR(
            work_province_id=self.work_province_id,
            work_other=self.work_other,
            expression_language=self.expression_language,
            work_date=self.work_date,
            expression_date=self.expression_date,
            expression_version=self.frbr_type + self.expression_version,
        )


class PubdataFRBRFactory(Factory):
    work_province_id: str = "pv28"
    work_other: str = "omgevingsvisie-1"
    expression_language: str = "nld"
    work_date: str = "2025"
    expression_date: str = "2025-11-25"
    expression_version: int

    def create(self) -> PubdataFRBR:
        return PubdataFRBR(
            work_province_id=self.work_province_id,
            work_other=self.work_other,
            expression_language=self.expression_language,
            work_date=self.work_date,
            expression_date=self.expression_date,
            expression_version=FRBRType.PUB_DATA + self.expression_version,
        )


class DoelFRBRFactory(Factory):
    work_province_id: str = "pv28"
    work_other: str = "omgevingsvisie-1"
    work_date: str = "2025"

    def create(self) -> DoelFRBR:
        return DoelFRBR(
            work_province_id=self.work_province_id,
            work_other=self.work_other,
            work_date=self.work_date,
        )


class ActFRBRFactory(Factory):
    work_country: str = "nl"
    work_province_id: str = "pv28"
    work_other: str = "omgevingsvisie-1"
    expression_language: str = "nld"
    work_date: str = "2025"
    expression_date: str = "2025-11-25"
    expression_version: int

    def create(self) -> ActFRBR:
        return ActFRBR(
            work_country=self.work_country,
            work_province_id=self.work_province_id,
            work_other=self.work_other,
            expression_language=self.expression_language,
            work_date=self.work_date,
            expression_date=self.expression_date,
            expression_version=FRBRType.ACT + self.expression_version,
        )


class InstellingDoelFactory(Factory):
    datum_juridisch_werkend_vanaf: str | None = None

    def create(self) -> InstellingDoel:
        return InstellingDoel(
            frbr=DoelFRBRFactory().create(),
            datum_juridisch_werkend_vanaf=self.datum_juridisch_werkend_vanaf,
        )
