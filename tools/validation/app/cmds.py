import subprocess
from typing import Dict, List
import os

import click
import helpers.geostandaarden as geostandaarden
from helpers.models import Schematron, Schemas
from helpers.helpers import compile_schematrons, empty_directory, generate_report_filename, list_files_recursive, report_contains_errors, resolve_namespace, resolve_namespaces, resolve_schemas, resolve_schematrons
import config


os.environ["SGML_CATALOG_FILES"] = config.SGML_CATALOG_FILES


@click.group()
def cli():
    """Validation commands."""
    pass


@click.command()
@click.argument("path")
def xsd_all(path):
    schemas: Dict[str, Schemas] = resolve_schemas(config.MODULES)
    files = list_files_recursive(path, ["xml", "gml"])

    for file in files:
        filename: str = os.path.basename(file)
        namespace = resolve_namespace(file)
        if not namespace in schemas:
            click.echo(click.style(f"Nothing to test {filename} against", fg="yellow"))
            continue
        for xsd in schemas.get(namespace).xsds:
            cmd = [
                    'xmllint',
                    '--catalogs',
                    '--schema',
                    xsd,
                    '--noout',
                    file,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                click.echo(
                    click.style(filename, fg="green") + click.style(f" against {xsd} is ") + click.style("valid", fg="green", bold=True))
            
            else:
                click.echo(
                    click.style(filename, fg="yellow") + click.style(f" against {xsd} ") + click.style("failed", fg="red", bold=True))
                click.echo(click.style(result.stderr,  fg="red"))


@click.command()
@click.argument("path")
def schematron_all(path):
    schemas: Dict[str, Schemas] = resolve_schemas(config.MODULES)

    empty_directory("./report")
    compile_schematrons(schemas)

    files = list_files_recursive(path, ["xml", "gml"])
    for file in files:
        namespaces: List[str] = resolve_namespaces(file)
        schematrons: List[Schematron] = resolve_schematrons(schemas, namespaces)
        if not schematrons:
            click.echo(click.style(f"Nothing to test {file} against", fg="yellow"))
            continue

        for schematron in schematrons:
            report_filename = generate_report_filename(path, file, schematron.local)
            cmd = [
                'java',
                '-jar',
                config.SAXON_JAR,
                f'-s:{file}',
                f'-xsl:{schematron.compiled_file}',
                f'-o:{report_filename}',
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            filename: str = os.path.basename(file)

            if result.returncode == 0:
                color = "red"
                if not report_contains_errors(report_filename):
                    color = "green"
                    os.remove(report_filename)
                click.echo(f"Report generated for {filename} with " + click.style(schematron.local, fg=color))

            else:
                click.echo(click.style(f"Could not generate report for {filename} with {schematron.local}", fg="red"))


@click.command()
@click.argument("prefix")
def geostandaarden_generate_files(prefix: str):
    geostandaarden.generate_files(prefix)


cli.add_command(xsd_all)
cli.add_command(schematron_all)
cli.add_command(geostandaarden_generate_files)


if __name__ == '__main__':
    cli()
