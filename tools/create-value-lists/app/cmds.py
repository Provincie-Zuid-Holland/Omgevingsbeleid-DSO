import click

from service import do_create_area_designations


@click.group()
def cli():
    """Value lists commands."""
    pass


@click.command()
def create_area_designations():
    do_create_area_designations()


cli.add_command(create_area_designations)


if __name__ == "__main__":
    cli()
