import click
from loguru import logger as log
# Reader
@click.group()
@click.pass_context
def reader(ctx):
    """

    Args:
      ctx: 

    Returns:

    """
    pass

@reader.command(help="Add a reader to the project.")
@click.argument('name')
@click.pass_context
def add(ctx, name):
    """

    Args:
      ctx: 
      name: 

    Returns:

    """
    # get reader
    # set id
    # splice into local config
    # persist config
    log.debug(f'Adding {name} to {ctx.obj["wd"]}')

@reader.command()
@click.argument('name')
@click.pass_context
def remove(ctx, name):
    """

    Args:
      ctx: 
      name: 

    Returns:

    """
    pass

@reader.command(help="lists all available reader plugins")
@click.pass_context
def list(ctx):
    """

    Args:
      ctx: 

    Returns:

    """
    readers = ctx.obj.rd_list()
    for key in readers:
        click.echo(f'- {key}:\t')

@reader.command(help='Configure the reader with given name')
@click.argument('name')
@click.option('--path', '-p', type=click.Path(file_okay=False), help='Directory to be read')
@click.option('--recursive', '-r', type=click.BOOL, help='should dbp recurse?', default=True)
@click.option('--pattern', '-P', type=click.STRING, help='overwrite the default search pattern of the reader')
@click.pass_context
def configure(ctx, name, path, recursive, pattern):
    """

    Args:
      ctx: 
      name: 
      path: 
      recursive: 
      pattern: 

    Returns:

    """
    
    pass

@reader.command(help='register a reader class plugin')
@click.argument('name')
@click.argument('path', type=click.Path(dir_okay=False, exists=True))
@click.option('--global', '-g', help='register globally, files are copied into plugin folder', default=False)
def register():
    """ """
    # branch if global
        # check wether class is valid, i.e. is a descendant of Reader
        # copy to source file pluginfolder (is that a good idea?)
        # rewrite global conf with updated plugin registry
    # branch if local
        # check wether class is valid
        # rewrite local configuration with a plugin registry
    pass

@reader.command(help='unregister a reader class plugin')
@click.argument('name')
@click.option('--global', '-g', help='register globally, files are copied into plugin folder', default=False)
def unregister():
    """ """
    # branch if global
        # check wether name exists in registry
        # delete source file from pluginfolder (is that a good idea?)
        # rewrite global conf with updated plugin registry
    # branch if local
        # check wether name exists in registry
        # rewrite local configuration with a plugin registry
    pass
