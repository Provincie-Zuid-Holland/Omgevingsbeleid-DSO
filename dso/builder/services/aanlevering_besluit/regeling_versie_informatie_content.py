from ....models import DocumentType
from ....services.utils.helpers import load_template
from ....services.utils.waardelijsten import RegelingType
from ...state_manager.state_manager import StateManager


class RegelingVersieInformatieContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        soort_regeling = self._get_soort_regeling()

        content = load_template(
            "akn/RegelingVersieInformatie.xml",
            soort_regeling=soort_regeling,
            regeling_frbr=self._state_manager.input_data.publication_settings.regeling_frbr,
            regeling=self._state_manager.input_data.regeling,
            provincie_ref=self._state_manager.input_data.publication_settings.provincie_ref,
            soort_bestuursorgaan=self._state_manager.input_data.publication_settings.soort_bestuursorgaan,
        )
        return content

    def _get_soort_regeling(self) -> str:
        document_type: DocumentType = self._state_manager.input_data.publication_settings.document_type.upper()
        return RegelingType[document_type].value
