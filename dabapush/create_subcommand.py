import click
from loguru import logger as log
import yaml
from .Configuration.ProjectConfiguration import ProjectConfiguration

# CREATE
@click.command()
@click.option('--interactive/--non-interactive', default=True, show_default=True, help='should we run an interactive prompt to create the configuration?')
@click.pass_context
def create(ctx, interactive):
    """

    Args:
      ctx: 

    Returns:

    """
    log.debug(f'Creating project in {ctx.obj["wd"]}')
    globconf = ctx.obj["globconf"]
    
    # Initialize configuration dict
    conf = ProjectConfiguration()

    if (interactive):
        conf.set_name(
            click.prompt('project name', type=str)
        )
        conf.set_author(
            click.prompt('author name (split several authors with ";")', type=str)
        )

    man_config = click.confirm("Should we configure readers and writers?")
    while (man_config == True):
        thing_to_configure = click.prompt('Reader/Writer?', default='Writer')
        if (thing_to_configure != 'Reader' and thing_to_configure != 'Writer'):
            log.debug(f'Try again')
        else:
            if (thing_to_configure == 'Reader'):
                log.debug(f'Configuring a Reader')
                reader_name = click.prompt('Which Reader should we configure')
                if (reader_name in globconf['plugins']['reader']):
                    if (not 'reader' in conf):
                        conf["reader"] = {}
                    conf["reader"]["someid"] = reader_name
                    log.debug(f'Success! Found the reader you\'re looking for!')
            if (thing_to_configure == 'Writer'):
                log.debug(f'Configuring a Reader')
            man_config = click.confirm('do another')
    with ctx.obj["locconf_path"].open('w') as file:
        yaml.dump(conf, file)