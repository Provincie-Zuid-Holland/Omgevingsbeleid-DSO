import hashlib

from dso.builder.state_manager.models import AssetContentData, FileContentData, OutputFile, StrContentData


def compute_sha512(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        return hashlib.sha512(data).hexdigest()


def compute_sha512_of_output_file(output_file: OutputFile):
    match output_file.content:
        case StrContentData():
            return hashlib.sha512(output_file.content.content.encode()).hexdigest()

        case FileContentData():
            return compute_sha512(output_file.content.source_path)

        case AssetContentData():
            raise NotImplementedError()
