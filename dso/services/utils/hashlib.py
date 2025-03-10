import hashlib

from ...act_builder.state_manager.models import (
    AssetContentData,
    DocumentContentData,
    OutputFile,
    PdfContentData,
    StrContentData,
)


def compute_sha512(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        return hashlib.sha512(data).hexdigest()


def compute_sha512_of_output_file(output_file: OutputFile):
    match output_file.content:
        case StrContentData():
            return hashlib.sha512(output_file.content.content.encode()).hexdigest()

        case AssetContentData():
            raise NotImplementedError()

        case PdfContentData():
            return hashlib.sha512(output_file.content.pdf.binary).hexdigest()

        case DocumentContentData():
            return hashlib.sha512(output_file.content.document.Binary).hexdigest()
