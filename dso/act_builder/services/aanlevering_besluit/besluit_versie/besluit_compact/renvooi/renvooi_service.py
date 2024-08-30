from urllib.parse import urljoin

import requests
from lxml import etree
from requests_toolbelt.multipart.encoder import MultipartEncoder

from .......exceptions import RenvooiInternalServerError, RenvooiUnauthorizedError, RenvooiUnkownError, RenvooiXmlError
from .......models import ActFRBR, RenvooiRegelingMutatie
from .......services.utils.helpers import load_template


class RenvooiService:
    def __init__(
        self,
        mutatie: RenvooiRegelingMutatie,
        componentnaam: str,
        wordt_frbr: ActFRBR,
        wordt_vrijektest: str,
    ):
        self._mutatie: RenvooiRegelingMutatie = mutatie
        self._componentnaam: str = componentnaam
        self._wordt_frbr: ActFRBR = wordt_frbr
        self._wordt_vrijektest: str = wordt_vrijektest

    def fetch_mutation(self) -> str:
        was_doc = self._get_was_xml()
        wordt_doc = self._get_wordt_xml()

        multipart_data = MultipartEncoder(
            fields={
                "scenario": "renvooi",
                "bhkv-schema-versie": "1.2.0",
                "docA": ("was.xml", was_doc, "application/xml"),
                "docB": ("wordt.xml", wordt_doc, "application/xml"),
                "validate": "0",
            }
        )
        headers = {
            "x-api-key": urljoin(self._mutatie.renvooi_api_key, "/regelingmutatie-maak"),
            "Content-Type": multipart_data.content_type,
        }

        response = requests.post(
            self._mutatie.renvooi_api_url,
            headers=headers,
            data=multipart_data,
        )

        match response.status_code:
            case 200:
                result: str = self._cleanup_xml(response.text)
                return result
            case 403:
                raise RenvooiUnauthorizedError(response.text)
            case 422:
                raise RenvooiXmlError(response.text)
            case 500:
                raise RenvooiInternalServerError(response.text)
            case _ as code:
                raise RenvooiUnkownError(response.text, code)

    def _get_was_xml(self) -> str:
        regeling_versie: str = load_template(
            "akn/besluit_versie/besluit_compact/renvooi/RenvooiRegelingVersie.xml",
            regeling_frbr=self._mutatie.was_regeling_frbr,
            regeling_vrijetekst=self._mutatie.was_regeling_vrijetekst,
        )
        return regeling_versie.strip()

    def _get_wordt_xml(self) -> str:
        regeling_versie: str = load_template(
            "akn/besluit_versie/besluit_compact/renvooi/RenvooiRegelingVersie.xml",
            regeling_frbr=self._wordt_frbr,
            regeling_vrijetekst=self._wordt_vrijektest,
        )
        return regeling_versie.strip()

    def _cleanup_xml(self, content: str) -> str:
        root = etree.fromstring(content.encode("utf-8"))

        if "componentnaam" in root.attrib:
            root.set("componentnaam", self._componentnaam)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
