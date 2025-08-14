from lxml import etree


class DataHintCleaner:
    def cleanup_xml(self, xml_content: str) -> str:
        root = etree.fromstring(xml_content)

        for element in root.xpath("//*[@*[starts-with(name(), 'data-hint-')]]"):
            attributes_to_remove = [attr for attr in element.attrib if attr.startswith("data-hint-")]
            for attr in attributes_to_remove:
                element.attrib.pop(attr)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
