import click

from gebiedsaanwijzigen.service import do_create_gebiedsaanwijzingen
from koop.service import do_create_waardelijsten


@click.group()
def cli():
    """Value lists commands."""
    pass


@click.command()
def create_gebiedsaanwijzingen():
    do_create_gebiedsaanwijzingen()


@click.command()
def create_koop_waardelijsten():
    do_create_waardelijsten()


cli.add_command(create_gebiedsaanwijzingen)
cli.add_command(create_koop_waardelijsten)


if __name__ == "__main__":
    cli()
