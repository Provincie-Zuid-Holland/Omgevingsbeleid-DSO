from pathlib import Path
from typing import Optional

import click

from .act_builder.builder import Builder
from .act_builder.state_manager.input_data.input_data_loader import InputData, InputDataLoader


@click.group()
def cli():
    """Validation commands."""


def build_input_data_from_dir(input_dir: str, json_file: str = "main.json"):
    main_file = f"{input_dir}/{json_file}"
    loader = InputDataLoader(main_file)
    input_data: InputData = loader.load()
    return input_data


def run_generate(input_dir: str, base_output_dir: Optional[str], json_file: str):
    data: InputData = build_input_data_from_dir(input_dir, json_file)

    if base_output_dir is None:
        base_output_dir = "./output"

    # mirror output path to input
    relative_path = str(Path(input_dir).relative_to(Path(input_dir).parents[0]))
    output_dir = Path(base_output_dir) / relative_path

    builder = Builder(data)
    builder.build_publication_files()
    builder.save_files(str(output_dir))


@click.command()
@click.argument("input_dir")
@click.argument("output_dir", required=False, default=None)
@click.option("--json-file", default="main.json", help="JSON file name")
def generate(input_dir: str, output_dir: Optional[str], json_file: str):
    run_generate(input_dir, output_dir, json_file)


@click.command()
@click.argument("input_dir")
@click.argument("output_dir", required=False, default=None)
def generate_all(input_dir: Optional[str], output_dir: Optional[str]):
    for path in Path(input_dir).rglob("main.json"):
        dir_with_main = path.parent
        run_generate(str(dir_with_main), output_dir)


cli.add_command(generate)
cli.add_command(generate_all)


if __name__ == "__main__":
    cli()
