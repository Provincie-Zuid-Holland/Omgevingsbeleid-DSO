import os
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from ....models import OwData, ProcedureStap, ProcedureVerloop, PublicationSettings, RegelingMutatie
from ....services.utils.helpers import load_json_data, load_xml_file
from ....services.utils.os import create_normalized_path
from .ambtsgebied import Ambtsgebied
from .besluit import Besluit
from .object_template_repository import ObjectTemplateRepository
from .regeling import Regeling
from .resource.asset.asset_repository import AssetRepository
from .resource.policy_object.policy_object_repository import PolicyObjectRepository
from .resource.resource_loader import ResourceLoader
from .resource.resources import Resources
from .resource.werkingsgebied.werkingsgebied_repository import WerkingsgebiedRepository


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
    ow_data: OwData

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PolicyObjectRepository: lambda v: v.to_dict() if v is not None else None,
            AssetRepository: lambda v: v.to_dict() if v is not None else None,
            WerkingsgebiedRepository: lambda v: v.to_dict() if v is not None else None,
            ObjectTemplateRepository: lambda v: v.to_dict() if v is not None else None,
        }

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

        publication_settings = PublicationSettings.from_json(main_config["publication_settings"])
        besluit = self._create_besluit(main_config["besluit"])
        regeling = self._create_regeling(main_config["regeling"])
        regeling_mutatie = self._create_regeling_mutation(main_config["regeling_mutatie"])
        regeling_vrijetekst_content = self._create_regeling_vrijetekst(main_config["regeling_vrijetekst"])

        procedure_verloop = self._create_procedure_verloop(
            publication_settings,
            main_config["procedure_verloop"],
        )

        resource_loader = ResourceLoader(
            main_config["resources"],
            self._base_dir,
            publication_settings,
        )
        resources: Resources = resource_loader.load()

        object_template_repository: ObjectTemplateRepository = ObjectTemplateRepository(
            main_config["object_template_repository"]
        )

        ambtsgebied = Ambtsgebied.from_json(main_config["ambtsgebied"])

        ow_data = OwData.from_json(main_config["ow_data"])

        data = InputData(
            publication_settings=publication_settings,
            besluit=besluit,
            regeling=regeling,
            regeling_vrijetekst=regeling_vrijetekst_content,
            regeling_mutatie=regeling_mutatie,
            procedure_verloop=procedure_verloop,
            resources=resources,
            object_template_repository=object_template_repository,
            ambtsgebied=ambtsgebied,
            ow_data=ow_data,
        )
        return data

    def _create_besluit(self, besluit_config: dict):
        besluit = Besluit.parse_obj(besluit_config)
        return besluit

    def _create_regeling(self, regeling_config: dict):
        regeling = Regeling.parse_obj(regeling_config)
        return regeling

    def _create_regeling_mutation(self, regeling_mutatie_config: dict):
        mutatie = RegelingMutatie.parse_obj(regeling_mutatie_config)
        xml_document_path = mutatie.was_regeling_vrijetekst
        content = load_xml_file(create_normalized_path(self._base_dir, xml_document_path))
        # overwrite input json with file content
        mutatie.was_regeling_vrijetekst = content
        return mutatie

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

    def _create_regeling_vrijetekst(self, xml_file_path: str) -> str:
        path = create_normalized_path(self._base_dir, xml_file_path)
        loaded_content = load_xml_file(path)
        return loaded_content
