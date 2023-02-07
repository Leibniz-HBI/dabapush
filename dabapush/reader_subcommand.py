"""CLI subcommands for reader manipulation"""
# pylint: disable=W0622
from typing import List

import click

from .Dabapush import Dabapush


# Reader
@click.group()
def reader():
    """reader command"""


@reader.command(help="Add a reader to the project.")
@click.option(
    "--parameter",
    "-p",
    multiple=True,
    help="add configuration for the reader in a key value format, e.g. pattern='*.ndjson'.",
)
@click.argument("type")
@click.argument("name")
@click.pass_context
def add(ctx: click.Context, parameter: List[str], type: str, name: str) -> None:
    """add a reader to the project"""
    params = dict(arg.split("=") for arg in parameter)
    db: Dabapush = ctx.obj
    db.rd_add(type, name)
    db.rd_update(name, params)
    db.pr_write()


@reader.command()
@click.argument("name")
@click.pass_context
def remove(ctx, name):
    """remove a reader from a project"""
    db: Dabapush = ctx.obj
    db.rd_rm(name)


@reader.command(help="lists all available reader plugins")
@click.pass_context
def list(ctx):
    """list all readers"""
    readers = ctx.obj.rd_list()
    for key in readers:
        click.echo(f"- {key}")


@reader.command(help="Configure the reader with given name")
@click.option(
    "--parameter",
    "-p",
    multiple=True,
    type=click.STRING,
    help="add configuration for the reader in a key value format, e.g. pattern='*.ndjson'.",
)
@click.argument("name")
@click.pass_context
def configure(ctx: click.Context, parameter: List[str], name: str):
    """add configuation to a reader"""

    params = dict(arg.split("=") for arg in parameter)
    db: Dabapush = ctx.obj
    db.rd_update(name, params)
    db.pr_write()
