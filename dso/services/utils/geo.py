import hashlib
import os
import re
from xml.etree import ElementTree

from utils.data import Publicatieinstructies
from utils.waardelijsten import InformatieObjectType, Provincie, WorkType


def extract_name(filename):
    # Strip prefix "locaties"
    if filename.startswith("locaties"):
        filename = filename[len("locaties_") :]

    # Strip postfix pattern "-vX.gml" where X can be any version number
    filename = re.sub(r"-v\d+\.gml$", "", filename)
    return filename


def parse_gml_metadata(gml_paths):
    namespaces = {"geo": "https://standaarden.overheid.nl/stop/imop/geo/"}

    dict_list = []
    for path in gml_paths:
        with open(path, "r") as file:
            content = file.read()
            tree = ElementTree.ElementTree(ElementTree.fromstring(content))
            FRBRWork = tree.find(".//geo:FRBRWork", namespaces=namespaces).text
            FRBRExpression = tree.find(".//geo:FRBRExpression", namespaces=namespaces).text
            file_hash = hashlib.md5(content.encode()).hexdigest()

        filename = os.path.basename(path)
        name = extract_name(filename)
        gio_filename = f"GIO_locaties_{name}.xml"
        single_gml_dict = {
            "FRBRWork": FRBRWork,
            "FRBRExpression": FRBRExpression,
            "soortWork": WorkType.Informatieobject.value,
            "heeftGeboorteregeling": "/akn/nl/act/pv28/2023/2_41",  # TODO
            "geo_bestandsnaam": filename,
            "bestandsnaam": gio_filename,
            "hash": file_hash,
            "eindverantwoordelijke": Provincie.Zuid_Holland.value,
            "maker": Provincie.Zuid_Holland.value,
            "naamInformatieObject": name,
            "officieleTitel": FRBRWork,
            "publicatieinstructie": Publicatieinstructies.TeConsolideren,
            "formaatInformatieobject": InformatieObjectType.Geoinformatieobject.value,
        }
        dict_list.append(single_gml_dict)

    return dict_list
