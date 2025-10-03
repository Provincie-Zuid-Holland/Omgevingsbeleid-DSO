import re
from enum import Enum
from typing import Dict, List

from bs4 import BeautifulSoup

from dso.act_builder.state_manager.input_data.besluit import Bijlage
from dso.act_builder.state_manager.input_data.resource.besluit_pdf.besluit_pdf import BesluitPdf
from dso.act_builder.state_manager.input_data.resource.besluit_pdf.besluit_pdf_repository import BesluitPdfRepository
from dso.act_builder.state_manager.state_manager import StateManager
from dso.models import PublicationSettings
from dso.services.ewid.ewid_service import EWIDService
from dso.services.tekst.tekst import Divisietekst
from dso.services.utils.helpers import load_template


class AppendixDestination(str, Enum):
    BILL = "BILL"
    ACT = "ACT"


class PdfTitleStrategy(str, Enum):
    TITLE = "TITLE"
    FRBR = "FRBR"
    FILENAME = "FILENAME"


class AppendicesService:
    _REF_BILL_PDF_PATTERN = r"\[REF_BILL_PDF:([^\]]+)\]"

    def __init__(self, state_manager: StateManager, pdf_title_strategy: PdfTitleStrategy = PdfTitleStrategy.FRBR):
        publication_settings: PublicationSettings = state_manager.input_data.publication_settings

        self._besluit_pdf_repository: BesluitPdfRepository = state_manager.input_data.resources.besluit_pdf_repository
        self._wid_prefix: str = (
            f"{publication_settings.provincie_id}_{publication_settings.regeling_frbr.Expression_Version}__"
        )
        self._ewid_services: Dict[AppendixDestination, EWIDService] = {
            AppendixDestination.BILL: state_manager.bill_ewid_service,
            AppendixDestination.ACT: state_manager.act_ewid_service,
        }
        self._pdf_title_strategy: PdfTitleStrategy = pdf_title_strategy

    def generate_xml(
        self,
        destination: AppendixDestination,
        appendices: List[Bijlage],
        eid_prefix: str = "",
    ) -> str:
        contents: List[str] = []

        for appendix in appendices:
            content = self._parse_appendix(destination, eid_prefix, appendix)
            contents.append(content)

        response: str = "\n".join(contents)
        return response

    def _parse_appendix(self, destination: AppendixDestination, eid_prefix: str, appendix: Bijlage) -> str:
        bijlage_eid: str = f"{eid_prefix}cmp_{appendix.nummer}"
        bijlage_wid: str = f"{self._wid_prefix}{bijlage_eid}"

        xml_content: str = self._html_to_xml_divisietekst(appendix.content)
        xml_content = self._replace_ref_bill_pdf(xml_content)

        ewid_service: EWIDService = self._ewid_services[destination]
        bijlage_content: str = ewid_service.add_ewids(
            xml_content,
            bijlage_eid,
            bijlage_wid,
            "Bijlage",
        )

        content = load_template(
            "akn/besluit_versie/Bijlage.xml",
            bijlage_eid=bijlage_eid,
            bijlage_wid=bijlage_wid,
            nummer=appendix.nummer,
            opschrift=appendix.opschrift,
            inhoud=bijlage_content,
        )

        return content

    def _html_to_xml_divisietekst(self, html: str) -> str:
        input_soup = BeautifulSoup(html, "html.parser")
        lichaam = Divisietekst()
        lichaam.consume_children(input_soup.children)

        output_soup = BeautifulSoup(features="xml")
        output = lichaam.as_xml(output_soup)
        output_xml = str(output)
        return output_xml

    def _replace_ref_bill_pdf(self, content: str) -> str:
        matches = re.findall(self._REF_BILL_PDF_PATTERN, content)
        for pdf_id in matches:
            pdf: BesluitPdf = self._besluit_pdf_repository.get(int(pdf_id))
            frbr: str = pdf.frbr.get_expression()
            link_title: str = self._get_link_title(pdf)
            search = f"[REF_BILL_PDF:{pdf_id}]"
            replacement = f"""<ExtRef soort="JOIN" ref="{frbr}">{link_title}</ExtRef>"""
            content = content.replace(search, replacement)

        return content

    def _get_link_title(self, pdf: BesluitPdf) -> str:
        match self._pdf_title_strategy:
            case PdfTitleStrategy.TITLE:
                return pdf.title
            case PdfTitleStrategy.FRBR:
                return pdf.frbr.get_expression()
            case PdfTitleStrategy.FILENAME:
                return pdf.filename
        raise RuntimeError("Not all cases for PdfTitleStrategy are implemented")
