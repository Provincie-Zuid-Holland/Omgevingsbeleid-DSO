import datetime
from typing import Optional

from dso.models import GioFRBR
from tests.factory import Factory


class GioFRBRFactory(Factory):
    Work_Province_ID: str = "pv28"
    Work_Other: str = "omgevingsvisie-1"
    Expression_Language: str = "nld"
    Work_Date: str = "2025"
    Expression_Date: str = "2025-11-25"
    Expression_Version: Optional[int] = None

    def create(self) -> GioFRBR:
        return GioFRBR(
            Work_Province_ID=self.Work_Province_ID,
            Work_Other=self.Work_Other,
            Expression_Language=self.Expression_Language,
            Work_Date=self.Work_Date,
            Expression_Date=self.Expression_Date,
            Expression_Version=self.Expression_Version,
        )
