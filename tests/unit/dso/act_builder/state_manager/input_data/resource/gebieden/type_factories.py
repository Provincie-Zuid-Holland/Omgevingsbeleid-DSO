from typing import Set, List

from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gio, GioLocatie
from dso.models import GioFRBR
from tests.factory import Factory
from tests.unit.dso.model_factories import GioFRBRFactory, FRBRType


class GioFactory(Factory):
    id: int
    gebied_ids: Set[int]
    new: bool = True
    geboorteregeling: str = "akn/nl/act/pv28/2024/omgevingsvisie-1"
    achtergrond_verwijzing: str = "TOP10NL"
    achtergrond_actualiteit: str = "2024-05-03"

    def create(self) -> Gio:
        source_codes: Set[str] = set([f"gebied-{id}" for id in self.gebied_ids])
        locaties: List[GioLocatie] = [GioLocatieFactory(id=id).create() for id in self.gebied_ids]
        gio_frbr: GioFRBR = GioFRBRFactory(Expression_Version=self.id, frbr_type=FRBRType.GEBIED).create()

        return Gio(
            source_codes=source_codes,
            locaties=locaties,
            title=f"GIO {self.id}",
            frbr=gio_frbr,
            new=self.new,
            geboorteregeling=self.geboorteregeling,
            achtergrond_verwijzing=self.achtergrond_verwijzing,
            achtergrond_actualiteit=self.achtergrond_actualiteit,
        )


class GioLocatieFactory(Factory):
    id: int

    def create(self) -> GioLocatie:
        return GioLocatie(
            code=f"gebied-{self.id}",
            title=f"Gebied {self.id}",
            basisgeo_id=f"gml-{self.id}",  # TODO fix
            gml=f'<gml:Point id="{self.id}" />',
        )
