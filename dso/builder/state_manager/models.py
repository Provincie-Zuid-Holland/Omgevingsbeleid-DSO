from abc import ABC
from dataclasses import dataclass, field

from dso.builder.state_manager.input_data.resource.asset.asset import Asset
from dso.models import ContentType


class ContentData(ABC):
    pass


class StrContentData(ContentData):
    def __init__(self, content: str):
        self.content: str = content


class AssetContentData(ContentData):
    def __init__(self, asset: Asset):
        self.asset: Asset = asset


@dataclass
class FileContentData(ContentData):
    def __init__(self, source_path: str):
        self.source_path: str = source_path


@dataclass
class OutputFile:
    filename: str
    content_type: ContentType
    content: ContentData
    options: dict = field(default_factory=dict)
