from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gebied
from dso.models import GioFRBR
from tests.factory import Factory, TypeEnum


class GebiedFactory(Factory):
    id: int
    frbr: GioFRBR
    new: bool = True
    geboorteregeling: str = "akn/nl/act/pv28/2024/omgevingsvisie-1"
    achtergrond_verwijzing: str = "TOP10NL"
    achtergrond_actualiteit: str = "2024-05-03"

    def create(self) -> Gebied:
        uuid = self.get_uuid_from_id(TypeEnum.GEBIED, self.id)
        return Gebied(
            title=f"Gebied {self.id}",
            code=f"gebied-{self.id}",
            frbr=self.frbr,
            uuid=uuid,
            identifier=f"wg-{self.id}-{uuid}",
            new=self.new,
            geboorteregeling=self.geboorteregeling,
            achtergrond_verwijzing=self.achtergrond_verwijzing,
            achtergrond_actualiteit=self.achtergrond_actualiteit,
            gml_id=f"gml-{self.id}",
            gml=f'<gml:Point id="{self.id}" />',
        )
