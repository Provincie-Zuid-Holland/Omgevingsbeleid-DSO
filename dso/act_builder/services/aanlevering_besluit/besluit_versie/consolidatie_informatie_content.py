from typing import Dict, List

from lxml import etree
from pydantic import BaseModel

from dso.act_builder.state_manager.input_data.resource.document.document import Document
from dso.act_builder.state_manager.states.text_manipulator.models import (
    TekstBijlageDocument,
    TextData,
    TekstBijlageGeoGio,
)
from ....state_manager.input_data.resource.gebieden.types import GeoGio
from ....state_manager.state_manager import StateManager
from ....state_manager.states.artikel_eid_repository import ArtikelEidType
from .....models import PublicationSettings, VerwijderdeGio
from .....services.utils.helpers import load_template


class ConsolidationWithdrawal(BaseModel):
    instrument: str
    eid: str


class Tijdstempel(BaseModel):
    doel: str
    datum: str
    eid: str


class BeoogdObject(BaseModel):
    instrument_versie: str
    eid: str


class ConsolidatieInformatieContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        settings: PublicationSettings = self._state_manager.input_data.publication_settings
        instelling_doel: str = settings.instelling_doel.frbr.get_work()
        text_data: TextData = self._state_manager.text_data

        beoogde_regeling = BeoogdObject(
            instrument_versie=settings.regeling_frbr.get_expression(),
            eid=self._state_manager.artikel_eid.find_one_by_type(ArtikelEidType.WIJZIG).eid,
        )

        beoogd_informatieobjecten: List[BeoogdObject] = []
        geogios_new: List[GeoGio] = self._state_manager.input_data.resources.geogio_repository.get_new()
        for gio in geogios_new:
            text_gio: TekstBijlageGeoGio = text_data.get_geogio_by_key(gio.key())
            beoogd_informatieobject = BeoogdObject(
                instrument_versie=gio.frbr.get_expression(),
                eid=f"!{settings.regeling_componentnaam}#{text_gio.eid}",
            )
            beoogd_informatieobjecten.append(beoogd_informatieobject)

        documents_new: List[Document] = self._state_manager.input_data.resources.document_repository.get_new()
        for document in documents_new:
            text_document: TekstBijlageDocument = text_data.get_document_by_code(document.Code)
            beoogd_informatieobject = BeoogdObject(
                instrument_versie=document.Frbr.get_expression(),
                eid=f"!{settings.regeling_componentnaam}#{text_document.eid}",
            )
            beoogd_informatieobjecten.append(beoogd_informatieobject)

        withdrawals: List[ConsolidationWithdrawal] = self._get_withdrawals()

        tijdstempels: List[Tijdstempel] = []
        if settings.instelling_doel.datum_juridisch_werkend_vanaf is not None:
            tijdstempel = Tijdstempel(
                doel=instelling_doel,
                datum=settings.instelling_doel.datum_juridisch_werkend_vanaf,
                eid=self._state_manager.artikel_eid.find_one_by_type(ArtikelEidType.BESLUIT_INWERKINGSTIJD).eid,
            )
            tijdstempels.append(tijdstempel)

        content = load_template(
            "akn/besluit_versie/ConsolidatieInformatie.xml",
            instelling_doel=instelling_doel,
            beoogde_regeling=beoogde_regeling,
            beoogd_informatieobjecten=beoogd_informatieobjecten,
            withdrawals=withdrawals,
            tijdstempels=tijdstempels,
        )
        return content

    def _get_withdrawals(self) -> List[ConsolidationWithdrawal]:
        if self._state_manager.input_data.regeling_mutatie is None:
            return []
        if self._state_manager.regeling_vrijetekst_aangeleverd is None:
            raise RuntimeError("Expecting 'regeling_vrijetekst_aangeleverd' to be set")

        """
        This parses the eid and ref from the vrijetekst

            <ExtIoRef eId="cmp_I__content_o_1__list_o_1__item_o_2__ref_o_1"
                wId="gm0297_1__cmp_I__content_o_1__list_o_2__ref_o_1"
                ref="/join/id/regdata/gm0297/2019/Centrumgebied/nld@2019-06-18;3520">
                    /join/id/regdata/gm0297/2019/Centrumgebied/nld@2019-06-18;3520
            </ExtIoRef>
        """
        ref_to_eid_map: Dict[str, str] = {}
        root = etree.fromstring(self._state_manager.regeling_vrijetekst_aangeleverd)
        ns = {"ns": "https://standaarden.overheid.nl/stop/imop/tekst/"}
        for extref in root.xpath(".//ns:ExtIoRef[@ref and @eId]", namespaces=ns):
            ref = extref.get("ref")
            eid = extref.get("eId")
            ref_to_eid_map[ref] = eid

        result: List[ConsolidationWithdrawal] = []
        component_name: str = self._state_manager.input_data.publication_settings.regeling_componentnaam
        removed_gios: List[VerwijderdeGio] = self._state_manager.input_data.regeling_mutatie.te_verwijderden_gios
        for removed_gio in removed_gios:
            expression: str = removed_gio.frbr.get_expression()
            eid: str = ref_to_eid_map.get(expression, "")
            work: str = removed_gio.frbr.get_work()

            if eid != "":
                eid = f"!{component_name}#{eid}"

            result.append(
                ConsolidationWithdrawal(
                    instrument=work,
                    eid=eid,
                )
            )

        return result
