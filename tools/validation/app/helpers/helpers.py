import os
import os.path
import shutil
from pprint import pprint
import subprocess
from typing import Dict, List, Optional, Set, Tuple

from pydantic import BaseModel
from lxml import etree

from config import SCHEMATRON_MAP
from helpers.models import Module, Schemas, Schematron


def empty_directory(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            shutil.rmtree(os.path.join(root, name))



def resolve_schemas(modules: List[Module]) -> Dict[str, Schemas]:
    result: Dict[str, Schemas] = {}

    for module in modules:
        with open(module.file, 'rb') as file:
            xml_content = file.read()

        # Parse the XML content using lxml
        root = etree.fromstring(xml_content)
        nsmap = module.nsmap

        for module in root.xpath('//ns:Module', namespaces=nsmap):
            ns = module.xpath('ns:namespace/text()', namespaces=nsmap)[0]

            schemas = module.xpath('.//ns:schema/text()', namespaces=nsmap)
            schematrons = module.xpath('.//ns:schematron/text()', namespaces=nsmap)
            result.setdefault(ns, Schemas())
            
            if schemas:
                result[ns].xsds.add(schemas[-1])
            if schematrons:
                original_schematron = schematrons[-1]
                if not original_schematron in SCHEMATRON_MAP:
                    raise Exception(f"Schematron {original_schematron} is not known to config.SCHEMATRON_MAP")
                schematron = Schematron(
                    original=original_schematron,
                    local=SCHEMATRON_MAP[original_schematron],
                )
                result[ns].schematrons.add(schematron)
    
    return result


def resolve_schematrons(schemas: Dict[str, Schemas], namespaces: List[str]) -> List[Schematron]:
    schematrons: Set[Schematron] = set()
    for namespace in namespaces:
        if not namespace in schemas:
            continue
        for schematron in schemas.get(namespace).schematrons:
            schematrons.add(schematron)

    return list(schematrons)


def list_files_recursive(directory, extensions=None):
    if extensions is None:
        extensions = []
    extensions = [e.lower() for e in extensions]
    
    all_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if os.path.splitext(filename)[1][1:].lower() in extensions:
                all_files.append(os.path.join(dirpath, filename))
    return all_files


def resolve_namespaces(path: str) -> List[str]:
    with open(path, 'rb') as file:
        xml_content = file.read()

    root = etree.fromstring(xml_content)
    namespaces = set()
    for element in root.iter():
        for k, v in element.nsmap.items():
            namespaces.add(v)

    return list(namespaces)


def resolve_namespace(path: str) -> Optional[str]:
    with open(path, 'rb') as file:
        xml_content = file.read()

    root = etree.fromstring(xml_content)
    namespace = root.nsmap[root.prefix]

    return namespace


def compile_schematrons(schemas: Dict[str, Schemas]) -> Dict[str, Schematron]:
    result = {}
    for ns, schema in schemas.items():
        for schematron in schema.schematrons:
            result[schematron.original] = schematron
            if not os.path.exists(schematron.step_1_file):
                print("creating step 1 file")
                ok, err = _compile(schematron.local_file, "./data/xslt/iso_dsdl_include.xsl", schematron.step_1_file)
                if not ok:
                    raise RuntimeError(err)
            if not os.path.exists(schematron.step_2_file):
                print("creating step 2 file")
                ok, err = _compile(schematron.step_1_file, "./data/xslt/iso_abstract_expand.xsl", schematron.step_2_file)
                if not ok:
                    raise RuntimeError(err)
            if not os.path.exists(schematron.compiled_file):
                print("creating compiled file")
                ok, err = _compile(schematron.step_2_file, "./data/xslt/iso_svrl_for_xslt2.xsl", schematron.compiled_file)
                if not ok:
                    raise RuntimeError(err)

    return result


def _compile(input: str, xsl: str, output: str) -> Tuple[bool, str]:
    cmd = [
        'java',
        '-jar',
        './saxon/saxon-he-11.6.jar',
        f'-s:{input}',
        f'-xsl:{xsl}',
        f'-o:{output}',
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        return True, ""
    else:
        return False, result.stderr


def generate_report_filename(base_path: str, filepath: str, schematron: str) -> str:
    relative_path = os.path.relpath(filepath, base_path)
    schematron = schematron.replace("/", "-")
    report_path = f"./report/{relative_path}-{schematron}.svrl"
    return report_path


def contains_text(filepath: str, search_text: str) -> bool:
    with open(filepath, 'r') as file:
        for line in file:
            if search_text in line:
                return True
    return False


def report_contains_errors(filepath: str) -> bool:
    return contains_text(filepath, "svrl:failed-assert")
