import os
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from ....models import ProcedureStap, ProcedureVerloop, PublicationSettings, RegelingMutatie
from ....services.utils.helpers import load_json_data
from .ambtsgebied import Ambtsgebied
from .besluit import Besluit
from .object_template_repository import ObjectTemplateRepository
from .regeling import Regeling
from .resource.resource_loader import ResourceLoader
from .resource.resources import Resources


class InputData(BaseModel):
    publication_settings: PublicationSettings
    besluit: Besluit
    regeling: Regeling
    regeling_vrijetekst: str
    regeling_mutatie: Optional[RegelingMutatie] = Field(None)
    procedure_verloop: ProcedureVerloop
    resources: Resources
    object_template_repository: ObjectTemplateRepository
    ambtsgebied: Ambtsgebied

    class Config:
        arbitrary_types_allowed = True

    def get_known_wid_map(self) -> Dict[str, str]:
        if self.regeling_mutatie is None:
            return {}
        return self.regeling_mutatie.bekend_wid_map

    def get_known_wids(self) -> List[str]:
        if self.regeling_mutatie is None:
            return []
        return self.regeling_mutatie.bekend_wids


class InputDataLoader:
    def __init__(self, main_file_path: str):
        self._main_file_path: str = main_file_path
        self._base_dir: str = os.path.dirname(main_file_path)

    def load(self) -> InputData:
        main_config: dict = load_json_data(self._main_file_path)

        publication_settings = PublicationSettings.from_json(main_config["settings"])
        besluit = self._create_besluit(main_config["besluit"])
        regeling = self._create_regeling(main_config["regeling"])
        regeling_vrijetekst = self._create_regeling_vrijetekst(main_config["regeling_vrijetekst"])

        procedure_verloop = self._create_procedure_verloop(
            publication_settings,
            main_config["procedure"],
        )

        resource_loader = ResourceLoader(
            main_config["resources"],
            self._base_dir,
            publication_settings,
        )
        resources: Resources = resource_loader.load()

        object_template_repository: ObjectTemplateRepository = ObjectTemplateRepository(main_config["object_templates"])

        data = InputData(
            publication_settings=publication_settings,
            besluit=besluit,
            regeling=regeling,
            regeling_vrijetekst=regeling_vrijetekst,
            procedure_verloop=procedure_verloop,
            resources=resources,
            object_template_repository=object_template_repository,
        )
        return data

    def _create_besluit(self, besluit_config: dict):
        besluit = Besluit.parse_obj(besluit_config)
        return besluit

    def _create_regeling(self, besluit_config: dict):
        besluit = Regeling.parse_obj(besluit_config)
        return besluit

    def _create_procedure_verloop(
        self,
        publication_settings: PublicationSettings,
        procedure_config: dict,
    ) -> ProcedureVerloop:
        stappen: List[ProcedureStap] = [ProcedureStap.parse_obj(s) for s in procedure_config["stappen"]]
        procedure_verloop = ProcedureVerloop(
            bekend_op=publication_settings.datum_bekendmaking,
            stappen=stappen,
        )
        return procedure_verloop

    def _create_regeling_vrijetekst(self, regeling_vrijetekst: Union[str, List[str]]) -> str:
        if isinstance(regeling_vrijetekst, list):
            return "".join(regeling_vrijetekst)
        return regeling_vrijetekst
