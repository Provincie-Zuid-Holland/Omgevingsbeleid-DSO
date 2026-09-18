from xml.etree import ElementTree

from dso.act_builder.state_manager import StateManager, OutputFile


class StateManagerTestCase:
    def _normalize_xml(self, xml: str) -> str:
        root = ElementTree.fromstring(xml)
        return ElementTree.tostring(root, encoding="unicode")

    def _get_output_file(self, state_manager: StateManager) -> OutputFile:
        args, _ = state_manager.add_output_file.call_args
        actual_file: OutputFile = args[0]
        return actual_file
