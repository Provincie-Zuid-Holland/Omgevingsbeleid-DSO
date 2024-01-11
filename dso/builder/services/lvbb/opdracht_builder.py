from ...services import BuilderService
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.state_manager import StateManager
from ....models import ContentType, OpdrachtType, PublicatieOpdracht
from ....services.utils.helpers import load_template


class OpdrachtBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        opdracht_file = self._create_opdracht_file(
            state_manager.input_data.publication_settings.opdracht,
        )
        state_manager.add_output_file(opdracht_file)

        return state_manager

    def _create_opdracht_file(self, opdracht: PublicatieOpdracht) -> OutputFile:
        template_file = self._get_template_file(opdracht.opdracht_type)

        content = load_template(
            template_file,
            pretty_print=True,
            opdracht=opdracht,
        )
        output_file = OutputFile(
            filename="opdracht.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file

    def _get_template_file(self, opdracht_type: OpdrachtType) -> str:
        match opdracht_type:
            case OpdrachtType.PUBLICATIE:
                return "templates/lvbb/opdracht/publicatie_opdracht.xml"
            case OpdrachtType.VALIDATIE:
                return "templates/lvbb/opdracht/validatie_opdracht.xml"
