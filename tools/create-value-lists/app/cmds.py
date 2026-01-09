import click

from service import do_create_gebiedsaanwijzingen


@click.group()
def cli():
    """Value lists commands."""
    pass


@click.command()
def create_gebiedsaanwijzingen():
    do_create_gebiedsaanwijzingen()


cli.add_command(create_gebiedsaanwijzingen)


if __name__ == "__main__":
    cli()
