import os
from typing import List, Optional, Set

from ...models import OwData
from ...services.ewid.ewid_service import EWIDService
from .input_data.input_data_loader import InputData
from .models import OutputFile
from .states import ArtikelEidRepository, OWStateRepository


class StateManager:
    def __init__(self, input_data: InputData):
        self.debug_enabled: bool = os.getenv("DEBUG_MODE", "").lower() in ("true", "1")
        self.debug: dict = {}

        self.input_data: InputData = input_data
        self.werkingsgebied_eid_lookup: dict = {}
        self.document_eid_lookup: dict = {}
        self.document_wid_lookup: dict = {}
        self.artikel_eid: ArtikelEidRepository = ArtikelEidRepository()
        self.ow_repository: OWStateRepository = OWStateRepository(input_data.ow_data, self.debug_enabled)
        self.output_files: List[OutputFile] = []
        # The full act text as how the conclusion would be
        self.regeling_vrijetekst_wordt: Optional[str] = None
        # What we send to DSO, might be different then `wordt` because of the renvooi
        self.regeling_vrijetekst_aangeleverd: Optional[str] = None
        self.used_asset_uuids: Set[str] = set()
        self.annotation_ref_lookup_map: dict = {}
        # result state of ow object data after processing
        self.ow_object_state: Optional[OwData] = None

        # Service is in the state manager
        # As we use it on multiple places, and the internal state should be updates for each use
        # @note: act_ewid_service is used within:
        #           <RegelingVrijetekst componentnaam="nieuweregeling"
        self.act_ewid_service: EWIDService = EWIDService(
            wid_prefix=f"{input_data.publication_settings.provincie_id}_{input_data.publication_settings.regeling_frbr.Expression_Version}",
            known_wid_map=input_data.get_known_wid_map(),
            known_wids=input_data.get_known_wids(),
        )
        self.bill_ewid_service: EWIDService = EWIDService(
            wid_prefix=f"{input_data.publication_settings.provincie_id}_{input_data.publication_settings.regeling_frbr.Expression_Version}",
        )

    def add_output_file(self, output_file: OutputFile):
        self.output_files.append(output_file)

    def add_output_files(self, output_files: List[OutputFile]):
        self.output_files.extend(output_files)

    def get_output_files(self) -> List[OutputFile]:
        output_files = sorted(self.output_files, key=lambda o: o.filename)
        return output_files

    def get_output_file_by_filename(self, filename: str) -> OutputFile:
        for output_file in self.output_files:
            if output_file.filename == filename:
                return output_file

        raise RuntimeError(f"Output file with filename {filename} not found")
