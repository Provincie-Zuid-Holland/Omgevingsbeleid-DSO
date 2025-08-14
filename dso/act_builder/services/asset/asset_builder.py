from typing import List

from ...builder_service import BuilderService
from ...state_manager.input_data.resource.asset.asset import Asset
from ...state_manager.input_data.resource.asset.asset_repository import AssetRepository
from ...state_manager.models import AssetContentData, OutputFile
from ...state_manager.state_manager import StateManager


class AssetBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        asset_repository: AssetRepository = state_manager.input_data.resources.asset_repository
        assets: List[Asset] = asset_repository.all()

        for asset in assets:
            if str(asset.UUID) not in state_manager.used_asset_uuids:
                continue

            output_file = OutputFile(
                filename=asset.get_filename(),
                content_type=asset.Meta.Formaat,
                content=AssetContentData(asset=asset),
            )
            state_manager.add_output_file(output_file)

        return state_manager
