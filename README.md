# Omgevingsbeleid-DSO

A Python library for generating STOP/TPOD-compliant publication packages for the Dutch Digital System for the Physical Environment (DSO - Digitaal Stelsel Omgevingswet), with current support for Omgevingsvisie and Programma document types.

## About

This tool, developed and maintained by Provincie Zuid-Holland, generates the required XML publication files for submitting environmental policies to the Dutch DSO platform. It enables provinces to create official Omgevingsvisie (Environmental Vision) and Programma (Program) publications that comply with national standards.

### Key Features

- Generates STOP/TPOD-compliant XML documents
- Creates publication packages for submission to LVBB (Landelijke Voorziening Bekendmaken en Beschikbaar stellen)
- Supports both draft and final ("vigerend") versions of regulations
- Handles geographic data (GML) and policy object relationships
- Produces announcement publications for draft acts

### What This Tool Does NOT Do

- Does not contain or manage policy text content
- Does not submit publications to the DSO platform
- Does not validate legal compliance of policy content

## Background: Dutch Environmental Act (Omgevingswet)

The Omgevingswet, effective since 2024, is a comprehensive reform of Dutch environmental law that consolidates regulations for:
- Spatial planning
- Construction
- Environment
- Water management
- Nature conservation

All Dutch provinces, municipalities, and water boards must publish their environmental policies digitally through the DSO platform, where citizens can view "Rules on the Map" and understand which regulations apply to specific locations.

## Installation

### Requirements

- Python 3.13+
- All dependencies listed in `requirements.txt`

### Setup

```bash
# Clone the repository
git clone https://github.com/Provincie-Zuid-Holland/Omgevingsbeleid-DSO.git
cd Omgevingsbeleid-DSO

# Install dependencies
make pip-sync
# or
pip install -r requirements.txt -r requirements-dev.txt
```

## Usage

### Command Line Interface

Generate a publication from an input scenario:

```bash
# Using make
make generate MAIN_FILE=./input/01-initial/main.json OUTPUT_DIR=./output/

# Using Python directly
python -m dso.cmds generate ./input/01-initial ./output/
```

### As a Python Library

```python
from dso.act_builder.builder import Builder
from dso.act_builder.state_manager.input_data.input_data_loader import InputDataLoader, InputData

# Load input configuration
loader = InputDataLoader("path/to/main.json")
input_data = loader.load()
# or construct the InputData directly
input_data = InputData(...)

# Create builder and generate publication
builder = Builder(input_data)
builder.build_publication_files()

# Save as files
builder.save_files("output_directory")

# Or get as ZIP buffer
zip_buffer = builder.zip_files()
```

## Input Data Structure

The tool requires structured input data in JSON format:

### Main Configuration (`main.json`)
- **Besluit**: Decision metadata (date, organization, title)
- **Regeling**: Regulation content and metadata
- **Procedure**: Procedural information

### Supporting Files
- `policy_objects.json`: Policy objects with rules and locations
- `werkingsgebieden.json`: Geographic areas where policies apply
- `assets.json`: Images and media files
- `regelingvrijetekst_template.xml`: Template for regulation text

## Output

The tool generates a publication package containing:

- **XML Documents**: STOP/TPOD-compliant XML files
- **GML Files**: Geographic data in GML format
- **Manifest Files**: Package metadata
- **Assets**: Images and other media files
- **Opdracht**: Submission instructions for LVBB

## Development

### Code Quality

```bash
# Auto-format code
make fix

```

### Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/unit/test_file.py -v

# Run with debugging
pytest -s
```

### Dependency Management

```bash
# Update dependencies
make pip-compile

# Upgrade all dependencies
make pip-upgrade
```

## Architecture

The library uses a Builder pattern with a central StateManager:

1. **Input Loading**: JSON configuration is loaded and validated
2. **State Building**: StateManager holds all the state for a build
3. **Service Pipeline**: Sequential application of builder services:
   - Opdracht (submission instructions)
   - Aanlevering Besluit (decision delivery)
   - OW (Omgevingswet objects)
   - GIO (Geographic information)
   - Documents and Assets
   - Manifest generation
4. **Output Generation**: Files are packaged for submission

## Standards Compliance

This tool implements:
- **STOP**: Standard for Official Publications (managed by KOOP)
- **TPOD**: Application Profiles for Environmental Documents (managed by Geonovum)
- **IMOW**: Information Model Environmental Act (Informatiemodel Omgevingswet)

## Validation

The `tools/validation/` directory contains utilities for validating generated XML against official schemas.

## Contributing

This project is publicly available and contributions are welcome. Please ensure:
- Code follows the existing style (use `make fix`)
- Tests pass (`pytest`)
- Documentation is updated

## License

EUPL-1.2 - See [LICENSE.md](LICENSE.md) for details.

## Support

For issues or questions:
- Create an issue on GitHub
- Contact the maintainers at Provincie Zuid-Holland

## Links

- [Official Publications (Officiële Bekendmakingen)](https://www.officielebekendmakingen.nl/)
- [DSO Information Point (IPLO)](https://iplo.nl/digitaal-stelsel/)
- [Geonovum Standards](https://www.geonovum.nl/geo-standaarden/omgevingswet)
- [KOOP Environmental Act Information](https://www.koopoverheid.nl/voor-overheden/gemeenten-provincies-en-waterschappen/omgevingswet)
- [Omgevingsbeleid-API by Zuid-Holland](https://github.com/Provincie-Zuid-Holland/Omgevingsbeleid-API)
