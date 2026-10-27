from uuid import UUID

from lxml import etree

from dso.act_builder.state_manager.input_data.resource.asset.asset import Asset
from dso.act_builder.state_manager.input_data.resource.asset.asset_repository import AssetRepository
from dso.act_builder.state_manager.state_manager import StateManager
from dso.act_builder.state_manager.states.text_manipulator.enricher.abstract_enricher import AbstractEnricher


class IllustrationEnricher(AbstractEnricher):
    def __init__(self, state_manager: StateManager):
        self._asset_repository: AssetRepository = state_manager.input_data.resources.asset_repository

    def enrich_xml(self, xml_content: str) -> str:
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_content.encode("utf-8"), parser)

        illustrations = root.xpath("//Illustratie[@data-hint-asset-uuid]")
        for illustration in illustrations:
            asset_uuid: str = illustration.get("data-hint-asset-uuid")
            asset: Asset = self._asset_repository.get(UUID(asset_uuid))

            illustration.set("breedte", str(asset.meta.breedte))
            illustration.set("dpi", str(asset.meta.dpi))
            illustration.set("formaat", asset.meta.formaat)
            illustration.set("hoogte", str(asset.meta.hoogte))
            illustration.set("naam", asset.get_filename())
            illustration.set("uitlijning", asset.meta.uitlijning)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
