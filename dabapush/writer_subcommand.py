import click

# Writer
@click.group()
def writer():
    """ """
    pass

@writer.command()
def add():
    """ """
    pass

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
