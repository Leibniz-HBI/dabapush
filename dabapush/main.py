import click
import sys
from loguru import logger as log

from .create_subcommand import create
from .run_subcommand import run
from .update_subcommand import update
from .discover_subcommand import discover
from .reader_subcommand import reader
from .writer_subcommand import writer
from .Dabapush import Dabapush

@click.group()
@click.option('--logfile', help='file to log in (optional)')
@click.option('--loglevel', default='INFO', help='the level to log, yk')
@click.pass_context
def cli(
    ctx: click.Context,
    logfile,
    loglevel
):
    """

    Args:
      ctx: 
      logfile: 
      loglevel: 

    Returns:

    """
    # prepare log options
    if (logfile != None):
        log.remove()
        if (loglevel == None):
            loglevel = 'DEBUG'
            log.add(sys.stdout, loglevel)
        log.add(logfile, loglevel)
    
    # prepare context
    ctx.ensure_object(Dabapush)

    db: Dabapush = ctx.obj
    log.debug(f'Starting DabaPush in {db.working_dir} from {db.install_dir}')

cli.add_command(reader)
cli.add_command(writer)
cli.add_command(run)
cli.add_command(create)
cli.add_command(discover)
cli.add_command(update)

if __name__ == '__main__':
    cli(obj = Dabapush())
