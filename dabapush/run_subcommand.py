import click
from loguru import logger as log

@click.command(help="Run the specified target, if specified target is 'all' all targets are run.")
@click.argument('target')
@click.pass_context
def run(ctx, target):
    """

    Args:
      ctx: 
      target: 

    Returns:

    """
    log.debug(f'Runrunrun {target} in {ctx.obj["wd"]}')
    log.debug(f'Using this global configuration {ctx.obj["globconf"]}')
    log.debug(f'Using this local configuration {ctx.obj["locconf"]}')
    pass