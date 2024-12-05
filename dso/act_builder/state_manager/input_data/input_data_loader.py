import json
import os
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from ....models import (
    OwData,
    ProcedureStap,
    ProcedureVerloop,
    PublicationSettings,
    RegelingMutatie,
    RenvooiRegelingMutatie,
    VervangRegelingMutatie,
)
from ....services.utils.helpers import load_json_data, load_xml_file
from ....services.utils.os import create_normalized_path
from .ambtsgebied import Ambtsgebied
from .besluit import Besluit
from .object_template_repository import ObjectTemplateRepository
from .regeling import Regeling
from .resource.asset.asset_repository import AssetRepository
from .resource.besluit_pdf.besluit_pdf_repository import BesluitPdfRepository
from .resource.policy_object.policy_object_repository import PolicyObjectRepository
from .resource.resource_loader import ResourceLoader
from .resource.resources import Resources
from .resource.werkingsgebied.werkingsgebied_repository import WerkingsgebiedRepository
from .resource.document.document_repository import DocumentRepository

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
            AssetRepository: lambda v: {k: w.dict() for k, w in v.to_dict().items()},
            WerkingsgebiedRepository: lambda v: {k: w.dict() for k, w in v.to_dict().items()},
            ObjectTemplateRepository: lambda v: v.to_dict() if v is not None else None,
            BesluitPdfRepository: lambda v: v.to_dict() if v is not None else None,
            DocumentRepository: lambda v: v.to_dict() if v is not None else None,
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

        if not main_config.get("regeling_mutatie"):
            regeling_mutatie = None
        else:
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
        mutatie = RegelingMutatie.from_dict(regeling_mutatie_config)
        match mutatie:
            case RenvooiRegelingMutatie():
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


class InputDataExporter:
    def __init__(self, input_data: InputData, output_dir: str = "output"):
        self._input_data: InputData = input_data
        self._output_dir: str = output_dir
        os.makedirs(self._output_dir, exist_ok=True)

    def to_dict(self) -> dict:
        return self._input_data.dict()

    def to_json(self) -> str:
        return self._input_data.json()

    def export_regelingvrijetekst_template(self, filename: str = "regelingvrijetekst_template.xml") -> None:
        xml_content = self._input_data.regeling_vrijetekst
        xml_file_path = os.path.join(self._output_dir, filename)
        with open(xml_file_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

    def export_was_regelingvrijetekst(self, filename: str = "was_regelingvrijetekst.xml") -> None:
        xml_content = self._input_data.regeling_mutatie.was_regeling_vrijetekst
        xml_file_path = os.path.join(self._output_dir, filename)
        with open(xml_file_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

    def export_policy_objects(self, filename: str = "policy_objects.json") -> None:
        policy_objects_dict = self._input_data.resources.policy_object_repository.to_dict()
        file_path = os.path.join(self._output_dir, filename)
        with open(file_path, "w") as file:
            json.dump(policy_objects_dict, file, indent=4)

    def export_assets(self, filename: str = "assets.json") -> None:
        asset_dict = self._input_data.resources.asset_repository.to_dict()
        file_path = os.path.join(self._output_dir, filename)
        with open(file_path, "w") as file:
            json.dump(asset_dict, file, indent=4)

    def export_werkingsgebieden(self, filename: str = "werkingsgebieden.json") -> None:
        werkingsgebied_dict = self._input_data.resources.werkingsgebied_repository.to_dict()
        file_path = os.path.join(self._output_dir, filename)
        with open(file_path, "w") as file:
            json.dump(werkingsgebied_dict, file, indent=4)

    def export_main_json(self, file_name: str = "main.json") -> None:
        """
        Export a single main.json file with all inputdata values.
        """
        file_path = os.path.join(self._output_dir, file_name)
        json_data = self._input_data.json(indent=4)
        with open(file_path, "w") as file:
            file.write(json_data)

    def export_dev_scenario(self) -> None:
        """
        Export the inputdata scenario as a dir with multiple files splitting:
            - templates
            - resources
            - main.json with updated references to the seperated files
        """

        # Parsed template
        self.export_regelingvrijetekst_template(filename="regelingvrijetekst_template.xml")

        # Resource files seperated
        self.export_policy_objects(filename="policy_objects.json")
        self.export_assets(filename="assets.json")
        self.export_werkingsgebieden(filename="werkingsgebieden.json")

        # Update main.json refs to seperated files
        regeling_vrijetekst_ref = "./regelingvrijetekst_template.xml"

        resources_ref = {
            "policy_object_repository": "./policy_objects.json",
            "asset_repository": "./assets.json",
            "werkingsgebied_repository": "./werkingsgebieden.json",
        }

        export_dict_updates = {
            "resources": resources_ref,
            "regeling_vrijetekst": regeling_vrijetekst_ref,
        }

        if self._input_data.regeling_mutatie:
            match self._input_data.regeling_mutatie:
                case RenvooiRegelingMutatie():
                    # dump was to file and update dict to reference the file
                    was_filename = "was_regelingvrijetekst.xml"
                    self.export_was_regelingvrijetekst(filename=was_filename)
                    regeling_mutatie_dict = self._input_data.regeling_mutatie.dict()
                    regeling_mutatie_dict.update(
                        {
                            "was_regeling_vrijetekst": f"./{was_filename}",
                            "type": "renvooi",
                            "renvooi_api_key": "placeholder",  # dont export api keys automatically
                        }
                    )
                case VervangRegelingMutatie():
                    regeling_mutatie_dict = self._input_data.regeling_mutatie.dict()
                    regeling_mutatie_dict.update({"type": "vervang"})
                case _:
                    raise RuntimeError("Missing clause")

            export_dict_updates["regeling_mutatie"] = regeling_mutatie_dict

        # replace the values for split file path refs in main.json
        updated_input_data = self._input_data.copy(update=export_dict_updates)

        file_path = os.path.join(self._output_dir, "main.json")
        with open(file_path, "w") as file:
            file.write(updated_input_data.json(indent=4))
