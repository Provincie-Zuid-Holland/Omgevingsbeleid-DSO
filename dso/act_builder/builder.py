import io
import os
from typing import Callable, Dict, List, Optional
from zipfile import ZIP_DEFLATED, ZipFile

from ..models import OwData
from ..services.assets.create_image import create_image, create_image_in_zip
from .services import BuilderService
from .services.aanlevering_besluit.aanlevering_besluit_builder import AanleveringBesluitBuilder
from .services.asset.asset_builder import AssetBuilder
from .services.geo.geo_informatie_object_vaststelling_builder import GeoInformatieObjectVaststellingBuilder
from .services.geo.gio_aanlevering_informatie_object_builder import GioAanleveringInformatieObjectBuilder
from .services.lvbb.manifest_builder import ManifestBuilder
from .services.lvbb.opdracht_builder import OpdrachtBuilder
from .services.ow.ow_builder_factory import OwBuilderFactory
from .services.pdf.pdf_aanlevering_informatie_object_builder import PdfAanleveringInformatieObjectBuilder
from .services.pdf.pdf_builder import PdfBuilder
from .state_manager.input_data.input_data_loader import InputData
from .state_manager.models import AssetContentData, PdfContentData, StrContentData
from .state_manager.state_manager import StateManager


class Builder:
    def __init__(self, input_data: InputData):
        self._state_manager: StateManager = StateManager(input_data)

        self._services: List[Callable[[], BuilderService]] = [
            lambda: OpdrachtBuilder(),
            lambda: AanleveringBesluitBuilder(),
            lambda: OwBuilderFactory.create_ow_builder(
                state_manager=self._state_manager,
                annotation_lookup_map=self._state_manager.annotation_ref_lookup_map,
                regeling_frbr=self._state_manager.input_data.publication_settings.regeling_frbr,
                doel_frbr=self._state_manager.input_data.publication_settings.instelling_doel.frbr,
            ),
            lambda: GeoInformatieObjectVaststellingBuilder(),
            lambda: GioAanleveringInformatieObjectBuilder(),
            lambda: PdfBuilder(),
            lambda: PdfAanleveringInformatieObjectBuilder(),
            lambda: AssetBuilder(),
            lambda: ManifestBuilder(),
        ]

    def build_publication_files(self):
        for service_factory in self._services:
            service = service_factory()
            self._state_manager = service.apply(self._state_manager)

    def save_files(self, output_dir: str):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for output_file in self._state_manager.get_output_files():
            destination_path = os.path.join(output_dir, output_file.filename)
            match output_file.content:
                case StrContentData():
                    with open(destination_path, "w") as f:
                        f.write(output_file.content.content)

                case AssetContentData():
                    create_image(output_file.content.asset, destination_path)

                case PdfContentData():
                    with open(destination_path, "wb") as f:
                        f.write(output_file.content.pdf.binary)

    def zip_files(self) -> io.BytesIO:
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, "a", ZIP_DEFLATED, False) as zip_file:
            for output_file in self._state_manager.get_output_files():
                match output_file.content:
                    case StrContentData():
                        zip_file.writestr(output_file.filename, output_file.content.content)

                    case AssetContentData():
                        create_image_in_zip(output_file.content.asset, zip_file, output_file.filename)

                    case PdfContentData():
                        zip_file.writestr(output_file.filename, output_file.content.pdf.binary)

        zip_buffer.seek(0)
        return zip_buffer

    def get_used_wid_map(self) -> Dict[str, str]:
        return self._state_manager.act_ewid_service.get_state_used_wid_map()

    def get_used_wids(self) -> List[str]:
        return self._state_manager.act_ewid_service.get_state_used_wids()

    def get_regeling_vrijetekst(self) -> Optional[str]:
        return self._state_manager.regeling_vrijetekst

    def get_ow_object_state(self) -> OwData:
        if self._state_manager.ow_object_state is None:
            raise RuntimeError("Expected OW object state result to be set in state manager.")
        return self._state_manager.ow_object_state
