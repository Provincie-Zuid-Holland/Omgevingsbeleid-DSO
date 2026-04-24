import click

from service import do_create_waardelijsten


@click.group()
def cli():
    """Value lists commands."""
    pass


@click.command()
def create_waardelijsten():
    do_create_waardelijsten()


cli.add_command(create_waardelijsten)


if __name__ == "__main__":
    cli()
