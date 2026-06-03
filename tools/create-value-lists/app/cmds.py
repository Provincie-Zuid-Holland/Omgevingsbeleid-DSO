import click

from .koop.service import do_create_waardelijsten as do_create_waardelijsten_koop
from .tpod.service import do_create_waardelijsten as do_create_waardelijsten_tpod


@click.group()
def cli():
    """Value lists commands."""
    pass


@click.command()
def create_waardelijsten_koop():
    do_create_waardelijsten_koop()


@click.command()
def create_waardelijsten_tpod():
    do_create_waardelijsten_tpod()


cli.add_command(create_waardelijsten_koop)
cli.add_command(create_waardelijsten_tpod)


if __name__ == "__main__":
    cli()
