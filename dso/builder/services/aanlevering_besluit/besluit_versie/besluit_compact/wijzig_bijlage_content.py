from ......models import PublicationSettings
from ......services.utils.helpers import load_template
from .....state_manager.state_manager import StateManager
from .wijzig_bijlage.bijlage_werkingsgebieden_content import BijlageWerkingsgebiedenContent
from .wijzig_bijlage.lichaam_content import LichaamContent


class WijzigBijlageContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        # bijlage_werkingsgebieden needs to go first because it changes the state_manager
        bijlage_werkingsgebieden: str = BijlageWerkingsgebiedenContent(self._state_manager).create()
        lichaam: str = LichaamContent(self._state_manager).create()
        settings: PublicationSettings = self._state_manager.input_data.publication_settings

        if self._state_manager.input_data.regeling_mutatie is not None:
            # When doing a mutation we need to create the RegelingVrijetekst
            # without the was/wordt/componentnaam attributes
            # As they needs to be in the wrapped RegelingMutatie tag
            regeling_vrijetekst: str = load_template(
                "akn/besluit_versie/besluit_compact/RegelingVrijetekst.xml",
                componentnaam=None,
                was=None,
                wordt=None,
                lichaam=lichaam,
                bijlage_werkingsgebieden=bijlage_werkingsgebieden,
                regeling_opschrift=self._state_manager.input_data.regeling.officiele_titel,
                componentnaam=settings.regeling_componentnaam,
            )

            regeling_content: str = load_template(
                "akn/besluit_versie/besluit_compact/RegelingMutatie.xml",
                componentnaam=settings.regeling_componentnaam,
                was=self._state_manager.input_data.regeling_mutatie.was_regeling_frbr.get_expression(),
                wordt=settings.regeling_frbr.get_expression(),
                regeling_vrijetekst=regeling_vrijetekst,
            )
        else:
            regeling_vrijetekst: str = load_template(
                "akn/besluit_versie/besluit_compact/RegelingVrijetekst.xml",
                componentnaam=settings.regeling_componentnaam,
                was=None,
                wordt=settings.regeling_frbr.get_expression(),
                lichaam=lichaam,
                bijlage_werkingsgebieden=bijlage_werkingsgebieden,
                regeling_opschrift=self._state_manager.input_data.regeling.officiele_titel,
            )
            regeling_content = regeling_vrijetekst

        # We store the regelingvrijetekst for the future mutation in case we implemented Renvooi
        self._state_manager.regeling_vrijetekst = regeling_vrijetekst

        content = load_template(
            "akn/besluit_versie/besluit_compact/WijzigBijlage.xml",
            regeling_content=regeling_content,
        )
        return content
