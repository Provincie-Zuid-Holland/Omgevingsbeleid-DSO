from abc import ABC
from dataclasses import dataclass, field

from dso.act_builder.state_manager.input_data.resource.document.document import Document

from ...models import ContentType
from .input_data.resource.asset.asset import Asset
from .input_data.resource.besluit_pdf.besluit_pdf import BesluitPdf


class ContentData(ABC):
    pass


class StrContentData(ContentData):
    def __init__(self, content: str):
        self.content: str = content


class AssetContentData(ContentData):
    def __init__(self, asset: Asset):
        self.asset: Asset = asset


class PdfContentData(ContentData):
    def __init__(self, pdf: BesluitPdf):
        self.pdf: BesluitPdf = pdf


class DocumentContentData(ContentData):
    def __init__(self, document: Document):
        self.document: Document = document


@dataclass
class OutputFile:
    filename: str
    content_type: ContentType
    content: ContentData
    options: dict = field(default_factory=dict)

    def to_dict(self):
        serializable_data = {
            "filename": self.filename,
            "content_type": self.content_type,
            "options": self.options,
        }
        if isinstance(self.content, StrContentData):
            serializable_data["content"] = str(self.content.content)
        else:
            serializable_data["content"] = None

        return serializable_data
