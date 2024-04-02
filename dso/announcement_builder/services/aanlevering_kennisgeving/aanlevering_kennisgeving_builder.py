from ....models import ContentType
from ....services.utils.helpers import load_template
from ...services import BuilderService
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.state_manager import StateManager
from .kennisgeving_versie.expression_identificatie_content import ExpressionIdentificatieContent
from .kennisgeving_versie.kennisgeving_content import KennisgevingContent
from .kennisgeving_versie.kennisgeving_metadata_content import KennisgevingMetadataContent
from .kennisgeving_versie.procedureverloop_content import ProcedureverloopContent


class AanleveringKennisgevingBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        akn_file = self._akn_file(state_manager)
        state_manager.add_output_file(akn_file)

        return state_manager

    def _akn_file(self, state_manager: StateManager) -> OutputFile:
        expression_identificatie = ExpressionIdentificatieContent(state_manager).create()
        metadata = KennisgevingMetadataContent(state_manager).create()
        procedureverloop = ProcedureverloopContent(state_manager).create()
        kennisgeving = KennisgevingContent(state_manager).create()

        content = load_template(
            "akn_kennisgeving/AanleveringKennisgeving.xml",
            pretty_print=True,
            expression_identificatie=expression_identificatie,
            metadata=metadata,
            procedureverloop=procedureverloop,
            kennisgeving=kennisgeving,
        )
        output_file = OutputFile(
            filename=state_manager.input_data.opdracht.publicatie_bestand,
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
