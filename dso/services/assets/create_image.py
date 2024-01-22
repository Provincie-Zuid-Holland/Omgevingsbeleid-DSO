import base64
import re
from zipfile import ZipFile

from ...builder.state_manager.input_data.resource.asset.asset import Asset


def decode_image_data(asset: Asset):
    match = re.match(r"data:image/(.*?);base64,(.*)", asset.Content)
    if not match:
        raise RuntimeError("Invalid asset content")
    _, base64_data = match.groups()
    return base64.b64decode(base64_data)


def create_image(asset: Asset, path: str):
    image_data = decode_image_data(asset)
    with open(path, "wb") as file:
        file.write(image_data)


def create_image_in_zip(asset: Asset, zip_file: ZipFile, filename: str):
    image_data = decode_image_data(asset)
    zip_file.writestr(filename, image_data)
