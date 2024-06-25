import click

from .act_builder.builder import Builder
from .act_builder.state_manager.input_data.input_data_loader import InputData, InputDataLoader


@click.group()
def cli():
    """Validation commands."""


@click.command()
@click.argument("input_dir")
@click.argument("output_dir")
@click.option("--json-file", default="main.json", help="JSON file name")
def generate(input_dir: str, output_dir: str, json_file: str):
    main_file = f"{input_dir}/{json_file}"
    loader = InputDataLoader(main_file)
    data: InputData = loader.load()

    builder = Builder(data)
    builder.build_publication_files()
    builder.save_files(output_dir)


cli.add_command(generate)


if __name__ == "__main__":
    cli()
