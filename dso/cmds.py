import click

from .act_builder.builder import Builder
from .act_builder.state_manager.input_data.input_data_loader import InputData, InputDataLoader


@click.group()
def cli():
    """Validation commands."""


@click.command()
@click.argument("input_dir")
@click.argument("output_dir")
def generate(input_dir: str, output_dir: str):
    main_file = f"{input_dir}/main.json"
    loader = InputDataLoader(main_file)
    data: InputData = loader.load()

    builder = Builder(data)
    builder.build_publication_files()
    builder.save_files(output_dir)


cli.add_command(generate)


if __name__ == "__main__":
    cli()
