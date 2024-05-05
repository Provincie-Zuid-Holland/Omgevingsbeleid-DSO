import re
from typing import List

from bs4 import BeautifulSoup

from ......models import PublicationSettings
from ......services.tekst.tekst import Divisietekst
from ......services.utils.helpers import load_template
from .....state_manager.input_data.besluit import Bijlage
from .....state_manager.input_data.resource.pdf.pdf import Pdf
from .....state_manager.input_data.resource.pdf.pdf_repository import PdfRepository
from .....state_manager.state_manager import StateManager


class BijlagenContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager
        self._pdf_repository: PdfRepository = state_manager.input_data.resources.pdf_repository
        self._ref_bill_pdf_pattern = r"\[REF_BILL_PDF:([^\]]+)\]"

    def create(self) -> str:
        bijlagen: List[Bijlage] = self._state_manager.input_data.besluit.bijlagen
        contents: List[str] = []

        for bijlage in bijlagen:
            content = self._parse_appendix(bijlage)
            contents.append(content)

        response: str = "\n".join(contents)
        return response

    def _parse_appendix(self, bijlage: Bijlage) -> str:
        settings: PublicationSettings = self._state_manager.input_data.publication_settings

        wid_prefix: str = f"{settings.provincie_id}_{settings.regeling_frbr.Expression_Version}__"
        bijlage_eid: str = f"cmp_{bijlage.nummer}"
        bijlage_wid: str = f"{wid_prefix}{bijlage_eid}"

        xml_content: str = self._html_to_xml_divisietekst(bijlage.content)
        xml_content = self._replace_ref_bill_pdf(xml_content)
        motivering_content: str = self._state_manager.act_ewid_service.add_ewids(
            xml_content,
            bijlage_eid,
            bijlage_wid,
            "Bijlage",
        )

        content = load_template(
            "akn/besluit_versie/besluit_compact/Bijlage.xml",
            bijlage_eid=bijlage_eid,
            bijlage_wid=bijlage_wid,
            nummer=bijlage.nummer,
            opschrift=bijlage.opschrift,
            inhoud=motivering_content,
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
        matches = re.findall(self._ref_bill_pdf_pattern, content)
        for pdf_id in matches:
            pdf: Pdf = self._pdf_repository.get(int(pdf_id))
            frbr: str = pdf.frbr.get_expression()
            search = f"[REF_BILL_PDF:{pdf_id}]"
            replacement = f"""<ExtRef soort="JOIN" ref="{frbr}">{frbr}</ExtRef>"""
            content = content.replace(search, replacement)

        return content
