import json
import urllib.request
from typing import Any, Dict


def load_json_data(source: str) -> Dict[str, Any]:
    """Load JSON data from either a file path or URL."""
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source) as response:
            return json.loads(response.read())
    else:
        with open(source, "r", encoding="utf-8") as f:
            return json.load(f)
