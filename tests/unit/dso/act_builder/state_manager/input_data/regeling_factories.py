from dso.act_builder.state_manager.input_data.regeling import Regeling
from dso.services.utils.waardelijsten import RechtsgebiedType, OnderwerpType
from tests.factory import Factory


class RegelingFactory(Factory):
    def create(self) -> Regeling:
        return Regeling(
            versienummer="1",
            officiele_titel="Omgevingsvisie van Zuid-Holland",
            citeertitel="Omgevingsvisie van Zuid-Holland",
            is_officieel="true",
            rechtsgebieden=[
                RechtsgebiedType.Omgevingsrecht,
            ],
            onderwerpen=[OnderwerpType.ruimtelijke_ordening],
        )
