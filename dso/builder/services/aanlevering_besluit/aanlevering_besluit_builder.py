from dso.builder.services import BuilderService
from dso.builder.services.aanlevering_besluit.besluit_versie_content import BesluitVersieContent
from dso.builder.services.aanlevering_besluit.regeling_versie_informatie_content import RegelingVersieInformatieContent
from dso.builder.state_manager.models import OutputFile, StrContentData
from dso.builder.state_manager.state_manager import StateManager
from dso.models import ContentType
from dso.services.utils.helpers import load_template


class AanleveringBesluitBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        akn_file = self._akn_file(state_manager)
        state_manager.add_output_file(akn_file)

        return state_manager

    def _akn_file(self, state_manager: StateManager) -> OutputFile:
        besluit_versie = BesluitVersieContent(state_manager).create()
        regeling_versie_informatie_content = RegelingVersieInformatieContent(state_manager).create()

        content = load_template(
            "templates/akn/AanleveringBesluit.xml",
            pretty_print=True,
            besluit_versie=besluit_versie,
            regeling_versie_informatie_content=regeling_versie_informatie_content,
        )
        output_file = OutputFile(
            filename=state_manager.input_data.publication_settings.opdracht.publicatie_bestand,
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
