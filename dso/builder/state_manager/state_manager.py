from typing import Dict, List, Optional

from pydantic import BaseModel

from ..state_manager.input_data.object_template_repository import ObjectTemplateRepository
from ..state_manager.input_data.resource.asset.asset_repository import AssetRepository
from ..state_manager.input_data.resource.policy_object.policy_object_repository import PolicyObjectRepository
from ..state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import WerkingsgebiedRepository
from ..state_manager.states.artikel_eid_repository import ArtikelEidRepository
from ..state_manager.states.ow_repository import OWStateRepository
from .input_data.input_data_loader import InputData
from .models import OutputFile
from .states.artikel_eid_repository import ArtikelEidRepository
from .states.ow_repository import OWStateRepository


class StateExport(BaseModel):
    input_data: Optional[InputData]
    werkingsgebied_eid_lookup: Optional[dict]
    object_tekst_lookup: Optional[dict]
    artikel_eid: Optional[ArtikelEidRepository]
    ow_repository: Optional[OWStateRepository]
    output_files: Optional[List[OutputFile]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PolicyObjectRepository: lambda v: v.to_dict() if v is not None else None,
            AssetRepository: lambda v: v.to_dict() if v is not None else None,
            WerkingsgebiedRepository: lambda v: v.to_dict() if v is not None else None,
            ObjectTemplateRepository: lambda v: v.to_dict() if v is not None else None,
            ArtikelEidRepository: lambda v: v.to_dict() if v is not None else None,
            OWStateRepository: lambda v: v.to_dict() if v is not None else None,
            OutputFile: lambda v: v.to_dict() if v is not None else None,
        }


class StateManager:
    def __init__(self, input_data: InputData):
        self.input_data: InputData = input_data
        self.werkingsgebied_eid_lookup: dict = {}
        self.object_tekst_lookup: dict = {}
        self.artikel_eid: ArtikelEidRepository = ArtikelEidRepository()
        self.ow_repository: OWStateRepository = OWStateRepository()
        self.output_files: List[OutputFile] = []
        self.debug: dict = {}

        # wId's used by indentifiers, for example beleidskeuze-4 by that object
        # Although it should be possible to add custom identifiers
        self.used_wid_map: Dict[str, str] = {}

        # All used wids, for export purposes
        # This will be send in the input data for the next version of this Act
        self.used_wids: List[str] = []

        self.regeling_vrijetekst: Optional[str] = None

    def add_output_file(self, output_file: OutputFile):
        self.output_files.append(output_file)

    def get_output_files(self) -> List[OutputFile]:
        output_files = sorted(self.output_files, key=lambda o: o.filename)
        return output_files

    def get_output_file_by_filename(self, filename: str) -> OutputFile:
        for output_file in self.output_files:
            if output_file.filename == filename:
                return output_file

        raise RuntimeError(f"Output file with filename {filename} not found")

    def build_state_export(self) -> StateExport:
        export = StateExport(
            input_data=self.input_data,
            werkingsgebied_eid_lookup=self.werkingsgebied_eid_lookup,
            object_tekst_lookup=self.object_tekst_lookup,
            artikel_eid=self.artikel_eid,
            ow_repository=self.ow_repository,
            output_files=self.output_files,
        )
        return export
