from ....models import ContentType
from ....services.utils.helpers import load_template
from ...builder_service import BuilderService
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.state_manager import StateManager
from .besluit_versie_content import BesluitVersieContent
from .regeling_versie_informatie_content import RegelingVersieInformatieContent


class AanleveringBesluitBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        akn_file = self._akn_file(state_manager)
        state_manager.add_output_file(akn_file)

        return state_manager

    def _akn_file(self, state_manager: StateManager) -> OutputFile:
        besluit_versie = BesluitVersieContent(state_manager).create()
        regeling_versie_informatie_content = RegelingVersieInformatieContent(state_manager).create()

        content = load_template(
            "akn/AanleveringBesluit.xml",
            pretty_print=False,
            besluit_versie=besluit_versie,
            regeling_versie_informatie_content=regeling_versie_informatie_content,
        )
        output_file = OutputFile(
            filename=state_manager.input_data.publication_settings.opdracht.publicatie_bestand,
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
