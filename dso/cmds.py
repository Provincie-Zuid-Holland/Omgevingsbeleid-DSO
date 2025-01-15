import shutil
from pathlib import Path
from typing import Optional

import click

from .act_builder.builder import Builder
from .act_builder.state_manager.input_data.input_data_loader import InputData, InputDataLoader
from .services.utils.load_json import load_json_data


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

    # Delete existing content of the output_dir
    if output_dir.exists() and output_dir.is_dir():
        shutil.rmtree(output_dir)

    builder = Builder(data)
    builder.build_publication_files()
    builder.save_files(str(output_dir))

    import pprint

    click.echo(click.style("---finished---", fg="green"))
    click.echo(click.style(f"DSO files saved in: {output_dir}", fg="green"))

    # output generate state values that are not in file output
    click.echo(click.style("Used WID MAP:", fg="green"))
    click.echo(pprint.pformat(builder.get_used_wid_map(), indent=2))

    click.echo(click.style("Used WID list:", fg="green"))
    click.echo(pprint.pformat(builder.get_used_wids(), indent=2))

    click.echo(click.style("OW data:", fg="green"))
    click.echo(builder.get_ow_object_state().json(indent=2))


@click.command()
@click.argument("input_dir")
@click.argument("output_dir", required=False, default=None)
@click.option("--json-file", default="main.json", help="JSON file name")
def generate(input_dir: str, output_dir: Optional[str], json_file: str):
    """Generate DSO package from a given input scenario using its scenario .json file."""
    run_generate(input_dir, output_dir, json_file)


@click.command()
@click.argument("input_dir")
@click.argument("output_dir", required=False, default=None)
@click.option("--json-file", default="main.json", help="JSON file name")
def generate_all(input_dir: Optional[str], output_dir: Optional[str], json_file: str):
    """Generate all DSO package files from multiple input scenarios in a directory."""
    for path in Path(input_dir).rglob("main.json"):
        dir_with_main = path.parent
        run_generate(str(dir_with_main), output_dir, json_file)


@click.command()
@click.option(
    "--json-file",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--json-url",
    type=str,
)
@click.option(
    "--type",
    "value_type",
    type=click.Choice(["all", "thema", "gebiedsaanwijzing", "gebiedsaanwijzing-groep"]),
    default="all",
    help="Which IMOW values to generate",
)
def generate_imow_value_lists(json_file: Optional[Path], json_url: Optional[str], value_type: str):
    """Generate IMOW value lists from a JSON file or URL."""
    from .services.ow.waardelijsten.imow_value_generator import IMOWValueGenerator

    if not json_file and not json_url:
        raise click.UsageError("Either --json-file or --json-url must be provided")
    if json_file and json_url:
        raise click.UsageError("Only one of --json-file or --json-url should be provided")

    source = str(json_file) if json_file else json_url
    try:
        json_data = load_json_data(source)
    except Exception as e:
        click.echo(click.style(f"Error loading JSON data: {str(e)}", fg="red"))
        return

    output_dir = Path(__file__).parent / "services" / "ow" / "waardelijsten" / "generated"
    if not output_dir.exists():
        raise click.UsageError(f"Output directory does not exist: {output_dir}")

    generator = IMOWValueGenerator(json_data=json_data, output_dir=output_dir)

    match value_type:
        case "all":
            results = generator.generate_all_values()
            click.echo(click.style("Generated IMOW value lists:", fg="green"))

            if results.thema.error:
                click.echo(click.style(f"Error generating thema values: {results.thema.error}", fg="red"))
            else:
                click.echo(f"- {results.thema.count} ThemaValue items")

            if results.gebiedsaanwijzing.error:
                click.echo(
                    click.style(
                        f"Error generating gebiedsaanwijzing values: {results.gebiedsaanwijzing.error}", fg="red"
                    )
                )
            else:
                click.echo(f"- {results.gebiedsaanwijzing.count} TypeGebiedsaanwijzingValue items")

            for result in results.gebiedsaanwijzing_groepen:
                if result.error:
                    click.echo(click.style(f"Error generating groep values: {result.error}", fg="red"))
                else:
                    click.echo(f"- {result.count} items in {result.output_file.name}")

            if not results.get_errors():
                click.echo("\nCreated files:")
                for file in results.get_created_files():
                    click.echo(f"- {file}")

        case "thema":
            result = generator.generate_thema_values()
            if result.error:
                click.echo(click.style(f"Error generating thema values: {result.error}", fg="red"))
            else:
                click.echo(click.style("Generated thema values:", fg="green"))
                click.echo(f"- {result.count} ThemaValue items")
                click.echo(f"\nCreated file: {result.output_file}")

        case "gebiedsaanwijzing":
            result = generator.generate_type_gebiedsaanwijzing_values()
            if result.error:
                click.echo(click.style(f"Error generating gebiedsaanwijzing values: {result.error}", fg="red"))
            else:
                click.echo(click.style("Generated gebiedsaanwijzing values:", fg="green"))
                click.echo(f"- {result.count} TypeGebiedsaanwijzingValue items")
                click.echo(f"\nCreated file: {result.output_file}")

        case "gebiedsaanwijzing-groep":
            results = generator.generate_gebiedsaanwijzing_groep_values()
            click.echo(click.style("Generated gebiedsaanwijzing groep values:", fg="green"))

            for result in results:
                if result.error:
                    click.echo(click.style(f"Error generating groep values: {result.error}", fg="red"))
                else:
                    click.echo(f"- {result.count} items in {result.output_file.name}")


cli.add_command(generate)
cli.add_command(generate_all)
cli.add_command(generate_imow_value_lists)


if __name__ == "__main__":
    cli()
