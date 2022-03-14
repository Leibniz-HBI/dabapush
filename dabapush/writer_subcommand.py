import click

# Writer
@click.group()
def writer():
    """ """
    pass

@writer.command()
@click.argument('type')
@click.argument('name')
@click.pass_context
def add(ctx, type: str, name: str):
    """ """
    ctx.obj.wr_add(type, name)
    ctx.obj.pr_write()

@writer.command()
def remove():
    """ """
    pass

@writer.command()
@click.pass_context
def list(ctx):
    """

    Parameters
    ----------
    ctx :
        

    Returns
    -------

    """
    writers = ctx.obj.wr_list()
    for key in writers:
        click.echo(f'- {key}:\t')

@writer.command()
def configure():
    """ """
    pass

@writer.command()
def register():
    """ """
    pass
