import re
from typing import Set

from lxml import etree

from ......models import PublicationSettings, RenvooiRegelingMutatie, VervangRegelingMutatie
from ......services.utils.helpers import load_template
from .....state_manager.state_manager import StateManager
from .renvooi.renvooi_service import RenvooiService
from .wijzig_bijlage.bijlage_werkingsgebieden_content import BijlageWerkingsgebiedenContent
from .wijzig_bijlage.lichaam_content import LichaamContent


class WijzigBijlageContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        # bijlage_werkingsgebieden needs to go first because it changes the state_manager
        bijlage_werkingsgebieden: str = BijlageWerkingsgebiedenContent(self._state_manager).create()
        lichaam: str = LichaamContent(self._state_manager).create()
        settings: PublicationSettings = self._state_manager.input_data.publication_settings

        # @note:
        # - aanleveren_regeling_content is what we provide to the DSO.
        #       This can be an initial RegelingVrijetekst (A), a VervangRegeling, or a renvooi RegelingMutatie.
        # - regeling_vrijetekst_wordt is how the RegelingVrijetekst would appear at the end.
        #       This is the same as with an initial regulation (case A); we store this in the environment cache
        regeling_vrijetekst_wordt, aanleveren_regeling_content = self._get_regeling_content(
            bijlage_werkingsgebieden,
            lichaam,
            settings,
        )

        used_asset_uuids: Set[str] = self._calculate_used_asset_uuids(aanleveren_regeling_content)
        self._state_manager.used_asset_uuids = used_asset_uuids

        # We store the RegelingVrijetekst for the future mutations
        self._state_manager.regeling_vrijetekst_wordt = regeling_vrijetekst_wordt
        self._state_manager.regeling_vrijetekst_aangeleverd = aanleveren_regeling_content

        wId_prefix: str = f"{settings.provincie_id}_{settings.regeling_frbr.Expression_Version}__"
        content = load_template(
            "akn/besluit_versie/besluit_compact/WijzigBijlage.xml",
            regeling_content=aanleveren_regeling_content,
            wId_prefix=wId_prefix,
            wijzig_bijlage=self._state_manager.input_data.besluit.wijzig_bijlage,
        )
        return content

    def _get_regeling_content(
        self,
        bijlage_werkingsgebieden: str,
        lichaam: str,
        settings: PublicationSettings,
    ) -> str:
        # The new final result
        regeling_vrijetekst_wordt: str = load_template(
            "akn/besluit_versie/besluit_compact/RegelingVrijetekst.xml",
            componentnaam=settings.regeling_componentnaam,
            was=None,
            wordt=settings.regeling_frbr.get_expression(),
            lichaam=lichaam,
            bijlage_werkingsgebieden=bijlage_werkingsgebieden,
            regeling_opschrift=self._state_manager.input_data.regeling.officiele_titel,
        )

        match self._state_manager.input_data.regeling_mutatie:
            case RenvooiRegelingMutatie():
                renvooi_service = RenvooiService(
                    mutatie=self._state_manager.input_data.regeling_mutatie,
                    componentnaam=settings.regeling_componentnaam,
                    wordt_frbr=settings.regeling_frbr,
                    wordt_vrijektest=regeling_vrijetekst_wordt,
                )
                regeling_content: str = renvooi_service.fetch_mutation()
                return regeling_vrijetekst_wordt, regeling_content

            case VervangRegelingMutatie():
                # When doing a VervangRegeling mutation we need to create the RegelingVrijetekst
                # without the was/wordt/componentnaam attributes
                # As those needs to be in the wrapped RegelingMutatie tag
                regeling_vrijetekst: str = load_template(
                    "akn/besluit_versie/besluit_compact/RegelingVrijetekst.xml",
                    componentnaam=None,
                    was=None,
                    wordt=None,
                    lichaam=lichaam,
                    bijlage_werkingsgebieden=bijlage_werkingsgebieden,
                    regeling_opschrift=self._state_manager.input_data.regeling.officiele_titel,
                )
                regeling_content: str = load_template(
                    "akn/besluit_versie/besluit_compact/RegelingMutatie.xml",
                    componentnaam=settings.regeling_componentnaam,
                    was=self._state_manager.input_data.regeling_mutatie.was_regeling_frbr.get_expression(),
                    wordt=settings.regeling_frbr.get_expression(),
                    regeling_vrijetekst=regeling_vrijetekst,
                )
                return regeling_vrijetekst_wordt, regeling_content
            case _:
                # What we send and what we store is the same for the initial regeling
                return regeling_vrijetekst_wordt, regeling_vrijetekst_wordt

    def _calculate_used_asset_uuids(self, aanleveren_regeling_content: str) -> Set[str]:
        # We only need to add images that are used in the resulting text.
        # - On an initial act that would be all the images
        # - On a regular renvooi that would be all current used, and removed images
        # - On a replace text that would be all current images
        # - The renvooi could deside to result into a replace text
        #
        # All in all, its safer to just check the text which images are used
        # and have that as the source of which images we should add to the zip
        parser: ActTextAssetParser = ActTextAssetParser()
        asset_uuids: Set[str] = parser.get_asset_uuids(aanleveren_regeling_content)
        return asset_uuids


class ActTextAssetParser:
    def __init__(self):
        self._uuid_regex = r"img_([a-f0-9\-]+)\.png"

    def get_asset_uuids(self, act_text: str) -> Set[str]:
        parser = etree.XMLParser(ns_clean=True)
        tree = etree.fromstring(act_text, parser)
        namespaces = {"ns": "https://standaarden.overheid.nl/stop/imop/tekst/"}
        illustraties = tree.xpath("//ns:Illustratie", namespaces=namespaces)

        asset_uuids: Set[str] = set()
        for illustratie in illustraties:
            uuidx = self._extract_uuid(illustratie.attrib.get("naam", ""))
            asset_uuids.add(uuidx)

        return asset_uuids

    def _extract_uuid(self, name: str) -> str:
        match = re.search(r"img_([a-f0-9\-]+)\.png", name)
        if match:
            return match.group(1)

        raise RuntimeError("Unable to find asset uuid in the name: '{name}'")
