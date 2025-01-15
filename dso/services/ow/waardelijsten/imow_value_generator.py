from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class GeneratorResult:
    count: int = 0
    output_file: Optional[Path] = None
    error: Optional[str] = None
    generated_code: Optional[str] = None


@dataclass
class IMOWValueGeneratorResults:
    IMOW_version: Optional[str] = None
    thema: GeneratorResult = field(default_factory=GeneratorResult)
    gebiedsaanwijzing: GeneratorResult = field(default_factory=GeneratorResult)
    gebiedsaanwijzing_groepen: List[GeneratorResult] = field(default_factory=list)

    def get_created_files(self) -> List[Path]:
        files = []
        for result in [self.thema, self.gebiedsaanwijzing, *self.gebiedsaanwijzing_groepen]:
            if result.output_file and not result.error:
                files.append(result.output_file)
        return files

    def get_errors(self) -> bool:
        return any(
            result.error is not None for result in [self.thema, self.gebiedsaanwijzing, *self.gebiedsaanwijzing_groepen]
        )


class IMOWCodeGenerator:
    def __init__(self, model_name: str, value_list_name: Optional[str] = None):
        self.model_name = model_name
        self.value_list_name = value_list_name.upper() if value_list_name else model_name.upper()

    def generate_imports(self) -> List[str]:
        return [
            f"from ..imow_models import {self.model_name}",
            "",
            "# Auto-generated from waardelijsten_IMOW JSON file",
            "# run cmds.py generate-imow-value-list command to create updated files.",
            "",
            f"{self.value_list_name}_ITEMS = [",
        ]

    def generate_value_code(self, waarde: Dict[str, Any], mapping: Dict[str, str]) -> str:
        value_code = f"    {self.model_name}(\n"
        for target_key, source_key in mapping.items():
            value = waarde.get(source_key, "")
            if isinstance(value, str):
                value = value.replace("'", "\\'")
            value_code += f"        {target_key}='{value}',\n"
        return value_code + "    ),"

    def generate_code(self, waarden: List[Dict[str, Any]], value_mapping: Optional[Dict[str, str]] = None) -> str:
        mapping = value_mapping or {"label": "label", "term": "term", "uri": "uri", "definitie": "definitie"}

        code = self.generate_imports()
        for waarde in waarden:
            code.append(self.generate_value_code(waarde, mapping))

        code.extend(["]", ""])
        return "\n".join(code)


class IMOWValueGenerator:
    def __init__(self, json_data: Dict[str, Any], output_dir: Path):
        self.json_data = json_data
        self.output_dir = output_dir
        self.results = IMOWValueGeneratorResults()

    def extract_imow_version(self) -> str:
        return self.json_data["waardelijsten"]["versie"]

    def extract_waarden(self, label: str) -> List[Dict[str, Any]]:
        for waardelijst in self.json_data["waardelijsten"]["waardelijst"]:
            if waardelijst["label"].lower() == label.lower() or waardelijst.get("titel", "").lower() == label.lower():
                return waardelijst["waarden"]["waarde"]
        return []

    def write_code_to_file(self, code: str, output_file: Path) -> None:
        output_file.write_text(code, encoding="utf-8")

    def generate_value_list(
        self,
        label: str,
        model_name: str,
        output_filename: str,
        value_mapping: Optional[Dict[str, str]] = None,
        value_list_name: Optional[str] = None,
    ) -> GeneratorResult:
        try:
            output_file = self.output_dir / output_filename
            waarden = self.extract_waarden(label)

            generator = IMOWCodeGenerator(model_name, value_list_name)
            generated_code = generator.generate_code(waarden, value_mapping)

            self.write_code_to_file(generated_code, output_file)

            return GeneratorResult(count=len(waarden), output_file=output_file, generated_code=generated_code)

        except Exception as e:
            return GeneratorResult(error=str(e))

    def generate_thema_values(self) -> GeneratorResult:
        result = self.generate_value_list(
            label="thema", model_name="ThemaValue", value_list_name="IMOW_THEMA", output_filename="imow_thema_values.py"
        )
        self.results.thema = result
        return result

    def generate_type_gebiedsaanwijzing_values(self) -> GeneratorResult:
        result = self.generate_value_list(
            label="type gebiedsaanwijzing",
            model_name="TypeGebiedsaanwijzingValue",
            value_list_name="IMOW_TYPE_GEBIEDSAANWIJZING",
            output_filename="imow_type_gebiedsaanwijzing_values.py",
        )
        self.results.gebiedsaanwijzing = result
        return result

    def generate_gebiedsaanwijzing_groep_values(self) -> List[GeneratorResult]:
        results = []
        gebiedsaanwijzing_types = self.extract_waarden("type gebiedsaanwijzing")

        output_file = self.output_dir / "imow_gebiedsaanwijzing_groep_values.py"
        all_groups_code = [
            "from ..imow_models import GebiedsaanwijzingGroepValue",
            "",
            "# Auto-generated from waardelijsten_IMOW JSON file",
            "# run cmds.py generate-imow-value-list command to create updated files.",
            "",
            "IMOW_GEBIEDSAANWIJZING_GROEP_ITEMS = [",
        ]

        total_count = 0
        for gtype in gebiedsaanwijzing_types:
            groep_label = f"{gtype['term']}groep"
            waarden = self.extract_waarden(groep_label)
            total_count += len(waarden)

            type_uri = gtype["uri"]
            for waarde in waarden:
                value_code = (
                    "    GebiedsaanwijzingGroepValue(\n"
                    f"        label='{waarde['label']}',\n"
                    f"        term='{waarde['term']}',\n"
                    f"        uri='{waarde['uri']}',\n"
                    f"        definitie='{waarde.get('definitie', '')}',\n"
                    f"        type_gebiedsaanwijzing='{type_uri}',\n"
                    "    ),"
                )
                all_groups_code.append(value_code)

        all_groups_code.extend(["", "]", ""])
        generated_code = "\n".join(all_groups_code)
        try:
            self.write_code_to_file(generated_code, output_file)
            result = GeneratorResult(count=total_count, output_file=output_file, generated_code=generated_code)
            results.append(result)
        except Exception as e:
            result = GeneratorResult(error=str(e))
            results.append(result)

        self.results.gebiedsaanwijzing_groepen = results
        return results

    def generate_all_values(self) -> IMOWValueGeneratorResults:
        """Generate all IMOW value lists."""
        self.results.IMOW_version = self.extract_imow_version()
        self.generate_thema_values()
        self.generate_type_gebiedsaanwijzing_values()
        self.generate_gebiedsaanwijzing_groep_values()
        return self.results
