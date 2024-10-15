from typing import Dict, List

from lxml import etree
from pydantic import BaseModel

from .....models import PublicationSettings, VerwijderdWerkingsgebied
from .....services.utils.helpers import load_template
from ....state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from ....state_manager.state_manager import StateManager
from ....state_manager.states.artikel_eid_repository import ArtikelEidType


class ConsolidationWithdrawal(BaseModel):
    instrument: str
    eid: str


class ConsolidatieInformatieContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        settings: PublicationSettings = self._state_manager.input_data.publication_settings
        instelling_doel: str = settings.instelling_doel.frbr.get_work()

        beoogde_regeling = {
            "instrument_versie": settings.regeling_frbr.get_expression(),
            "eid": self._state_manager.artikel_eid.find_one_by_type(ArtikelEidType.WIJZIG).eid,
        }

        beoogd_informatieobjecten = []
        werkingsgebieden: List[Werkingsgebied] = (
            self._state_manager.input_data.resources.werkingsgebied_repository.all()
        )
        for werkingsgebied in werkingsgebieden:
            if werkingsgebied.New:
                eid: str = self._state_manager.werkingsgebied_eid_lookup[str(werkingsgebied.UUID)]
                beoogd_informatieobjecten.append(
                    {
                        "instrument_versie": werkingsgebied.Frbr.get_expression(),
                        "eid": f"!{settings.regeling_componentnaam}#{eid}",
                    }
                )

        withdrawals: List[ConsolidationWithdrawal] = self._get_withdrawals()

        tijdstempels = []
        if settings.instelling_doel.datum_juridisch_werkend_vanaf is not None:
            tijdstempels.append(
                {
                    "doel": instelling_doel,
                    "datum": settings.instelling_doel.datum_juridisch_werkend_vanaf,
                    "eid": self._state_manager.artikel_eid.find_one_by_type(ArtikelEidType.BESLUIT_INWERKINGSTIJD).eid,
                }
            )

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
        removed_gios: List[VerwijderdWerkingsgebied] = (
            self._state_manager.input_data.regeling_mutatie.te_verwijderden_werkingsgebieden
        )
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
