from dso.act_builder.state_manager.input_data.regeling import Regeling
from dso.services.koop.waardelijsten.gen import TopLijst, BwbRechtgebied
from tests.factory import Factory


class RegelingFactory(Factory):
    def create(self) -> Regeling:
        return Regeling(
            versienummer="1",
            officiele_titel="Omgevingsvisie van Zuid-Holland",
            citeertitel="Omgevingsvisie van Zuid-Holland",
            is_officieel="true",
            rechtsgebieden=[
                BwbRechtgebied.Omgevingsrecht,
            ],
            onderwerpen=[TopLijst.RuimtelijkeOrdening],
        )
