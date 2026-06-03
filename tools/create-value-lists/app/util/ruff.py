import subprocess
import tempfile
from pathlib import Path


def format_with_ruff(code: str) -> str:
    with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp_path: Path = Path(tmp.name)

    subprocess.run(["ruff", "check", "--fix", str(tmp_path)], check=True)
    subprocess.run(["ruff", "format", str(tmp_path)], check=True)

    formatted: str = tmp_path.read_text()
    tmp_path.unlink()

    return formatted
