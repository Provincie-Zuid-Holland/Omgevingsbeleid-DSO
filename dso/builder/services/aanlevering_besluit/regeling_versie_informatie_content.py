from ....models import DocumentType
from ....services.utils.helpers import load_template
from ....services.utils.waardelijsten import RegelingType
from ...state_manager.state_manager import StateManager


class RegelingVersieInformatieContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        regeling_metadata: str = self._get_regeling_metadata()

        content = load_template(
            "akn/RegelingVersieInformatie.xml",
            regeling_metadata=regeling_metadata,
            regeling_frbr=self._state_manager.input_data.publication_settings.regeling_frbr,
            regeling=self._state_manager.input_data.regeling,
        )
        return content

    def _get_soort_regeling(self) -> str:
        document_type: DocumentType = self._state_manager.input_data.publication_settings.document_type.value
        return RegelingType[document_type].value

    def _get_regeling_metadata(self) -> str:
        # Regeling metadata is only needed for initial version
        if self._state_manager.input_data.regeling_mutatie is not None:
            return ""

        soort_regeling = self._get_soort_regeling()

        content = load_template(
            "akn/RegelingMetadata.xml",
            soort_regeling=soort_regeling,
            regeling_frbr=self._state_manager.input_data.publication_settings.regeling_frbr,
            regeling=self._state_manager.input_data.regeling,
            provincie_ref=self._state_manager.input_data.publication_settings.provincie_ref,
            soort_bestuursorgaan=self._state_manager.input_data.publication_settings.soort_bestuursorgaan,
        )
        return content
