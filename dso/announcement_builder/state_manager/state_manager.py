import os
from typing import List

from ...services.ewid.ewid_service import EWIDService
from .models import InputData, OutputFile


class StateManager:
    def __init__(self, input_data: InputData):
        self.debug_enabled: bool = os.getenv("DEBUG_MODE", "").lower() in ("true", "1")
        self.debug: dict = {}

        self.input_data: InputData = input_data
        self.output_files: List[OutputFile] = []

        # Service is in the state manager
        # As we use it on multiple places, and the internal state should be updates for each use
        # @note: act_ewid_service is used within:
        #           <RegelingVrijetekst componentnaam="nieuweregeling"
        self.act_ewid_service: EWIDService = EWIDService(
            wid_prefix=f"{input_data.provincie_id}_{input_data.bekendmaking_frbr.Expression_Version}",
        )
        self.bill_ewid_service: EWIDService = EWIDService(
            wid_prefix=f"{input_data.provincie_id}_{input_data.bekendmaking_frbr.Expression_Version}",
        )

    def add_output_file(self, output_file: OutputFile):
        self.output_files.append(output_file)

    def get_output_files(self) -> List[OutputFile]:
        output_files = sorted(self.output_files, key=lambda o: o.filename)
        return output_files
