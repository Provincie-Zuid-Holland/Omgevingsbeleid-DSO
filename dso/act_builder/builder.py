import io
import os
from typing import Dict, List, Optional, Set
from zipfile import ZIP_DEFLATED, ZipFile

from dso.act_builder.services.document.document_aanlevering_informatie_object_builder import DocumentAanleveringInformatieObjectBuilder
from dso.act_builder.services.document.document_builder import DocumentBuilder

from ..models import OwData
from ..services.assets.create_image import create_image, create_image_in_zip
from .services import BuilderService
from .services.aanlevering_besluit.aanlevering_besluit_builder import AanleveringBesluitBuilder
from .services.asset.asset_builder import AssetBuilder
from .services.besluit_pdf.besluit_pdf_aanlevering_informatie_object_builder import (
    BesluitPdfAanleveringInformatieObjectBuilder,
)
from .services.besluit_pdf.besluit_pdf_builder import BesluitPdfBuilder
from .services.geo.geo_informatie_object_vaststelling_builder import GeoInformatieObjectVaststellingBuilder
from .services.geo.gio_aanlevering_informatie_object_builder import GioAanleveringInformatieObjectBuilder
from .services.lvbb.manifest_builder import ManifestBuilder
from .services.lvbb.opdracht_builder import OpdrachtBuilder
from .services.ow.ow_builder_facade import OwBuilderFacade
from .state_manager.input_data.input_data_loader import InputData
from .state_manager.models import AssetContentData, DocumentContentData, PdfContentData, StrContentData
from .state_manager.state_manager import StateManager


class Builder:
    def __init__(self, input_data: InputData):
        self._state_manager: StateManager = StateManager(input_data)

        self._services: List[BuilderService] = [
            OpdrachtBuilder(),
            AanleveringBesluitBuilder(),
            OwBuilderFacade(),
            GeoInformatieObjectVaststellingBuilder(),
            GioAanleveringInformatieObjectBuilder(),
            BesluitPdfBuilder(),
            BesluitPdfAanleveringInformatieObjectBuilder(),
            DocumentBuilder(),
            DocumentAanleveringInformatieObjectBuilder(),
            AssetBuilder(),
            ManifestBuilder(),
        ]

    def build_publication_files(self):
        for service in self._services:
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

                case DocumentContentData():
                    with open(destination_path, "wb") as f:
                        f.write(output_file.content.document.binary)

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

                    case DocumentContentData():
                        zip_file.writestr(output_file.filename, output_file.content.document.Binary)

        zip_buffer.seek(0)
        return zip_buffer

    def get_used_asset_uuids(self) -> Set[str]:
        return self._state_manager.used_asset_uuids

    def get_used_wid_map(self) -> Dict[str, str]:
        return self._state_manager.act_ewid_service.get_state_used_wid_map()

    def get_used_wids(self) -> List[str]:
        return self._state_manager.act_ewid_service.get_state_used_wids()

    def get_regeling_vrijetekst(self) -> Optional[str]:
        return self._state_manager.regeling_vrijetekst_wordt

    def get_ow_object_state(self) -> OwData:
        if self._state_manager.ow_object_state is None:
            raise RuntimeError("Expected OW object state result to be set in state manager.")
        return self._state_manager.ow_object_state
