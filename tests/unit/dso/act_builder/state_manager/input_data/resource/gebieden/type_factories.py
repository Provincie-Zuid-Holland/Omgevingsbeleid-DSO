from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gebied
from dso.models import GioFRBR
from tests.factory import Factory, TypeEnum


class GebiedFactory(Factory):
    id: int
    title: str
    code: str
    frbr: GioFRBR
    new: bool = True
    geboorteregeling: str = ""
    achtergrond_verwijzing: str = ""
    achtergrond_actualiteit: str = ""
    gml_id: str = ""
    gml: str = ""

    def create(self) -> Gebied:
        uuid = self.get_uuid_from_id(TypeEnum.GEBIED, self.id)
        return Gebied(
            title=self.title,
            code=self.code,
            frbr=self.frbr,
            uuid=uuid,
            identifier=f"wg-{self.id}-{uuid}",
            new=self.new,
            geboorteregeling=self.geboorteregeling,
            achtergrond_verwijzing=self.achtergrond_verwijzing,
            achtergrond_actualiteit=self.achtergrond_actualiteit,
            gml_id=self.gml_id,
            gml=self.gml,
        )
