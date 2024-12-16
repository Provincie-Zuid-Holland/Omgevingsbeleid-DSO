import json
from pathlib import Path

from models import WaardelijstenRoot

INPUT_JSON = "waardelijsten_IMOW_v4.2.0.json"
OUTPUT_FILE = Path("waardelijsten.py")


def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    root = WaardelijstenRoot(**data)

    version = root.waardelijsten.versie
    value_lists = root.waardelijsten.waardelijst

    lines = [
        "# This file is auto-generated. Do not edit manually.",
        f"# Generated from version: {version}",
        "",
        "from .models import ValueEntry, ValueList, Symboolcode, CodeEntry, Waarden",
        "",
        f"VERSION = '{version}'",
        "",
    ]

    for vl in value_lists:
        var_name = vl.label.upper().replace(" ", "_")

        value_entry_lines = []
        for entry in vl.waarden.waarde:
            if entry.symboolcode is None:
                symboolcode_str = "None"
            elif isinstance(entry.symboolcode, str):
                symboolcode_str = repr(entry.symboolcode)
            else:

                def code_entry_str(ce):
                    return f"CodeEntry(id={ce.id!r}, content={ce.content!r})"

                parts = []
                for field_name in ["lijn", "punt", "vlak"]:
                    ce = getattr(entry.symboolcode, field_name)
                    if ce is None:
                        parts.append(f"{field_name}=None")
                    else:
                        parts.append(f"{field_name}={code_entry_str(ce)}")
                symboolcode_str = f"Symboolcode({', '.join(parts)})"

            value_entry_lines.append(
                f"ValueEntry("
                f"label={entry.label!r}, term={entry.term!r}, uri={entry.uri!r}, "
                f"definitie={entry.definitie!r}, toelichting={entry.toelichting!r}, "
                f"bron={entry.bron!r}, domein={entry.domein!r}, "
                f"specialisatie={entry.specialisatie!r}, symboolcode={symboolcode_str}"
                f")"
            )

        entries_str = ",\n        ".join(value_entry_lines)

        lines.append(
            f"{var_name}_VALUES = ValueList("
            f"label={vl.label!r}, titel={vl.titel!r}, uri={vl.uri!r}, type={vl.type!r}, "
            f"omschrijving={vl.omschrijving!r}, toelichting={vl.toelichting!r}, "
            f"version=VERSION, waarden=Waarden(waarde=[\n        {entries_str}\n    ])"
            f")\n"
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {OUTPUT_FILE} successfully.")


if __name__ == "__main__":
    main()
