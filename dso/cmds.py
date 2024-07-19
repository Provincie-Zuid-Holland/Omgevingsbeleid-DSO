from email.policy import default
import click
from pathlib import Path
from typing import Optional


from .act_builder.builder import Builder
from .act_builder.state_manager.input_data.input_data_loader import InputData, InputDataLoader


@click.group()
def cli():
    """Validation commands."""


@click.command()
@click.argument("input_dir")
@click.argument("output_dir", required=False, default=None)
@click.option("--json-file", default="main.json", help="JSON file name")
def generate(input_dir: str, output_dir: Optional[str], json_file: str):
    main_file = f"{input_dir}/{json_file}"
    loader = InputDataLoader(main_file)
    data: InputData = loader.load()

    if output_dir is None:
        # Get the last folder name from the input path
        last_folder = Path(input_dir).parts[-1]
        # Set the default output directory
        output_dir = f"./output/{last_folder}"

    builder = Builder(data)
    builder.build_publication_files()
    builder.save_files(output_dir)


cli.add_command(generate)


if __name__ == "__main__":
    cli()
