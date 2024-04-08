import os

import click
from autodoc.services import AIAutodocService
from autodoc.clients import Config
from .runner import Runner
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


@click.group()
def cli():
    pass

@click.command()
@click.option('--mode', '-m', type=click.Choice(['folder', 'file']), default='folder', help='Mode of operation: folder or file.')
@click.option('--format', is_flag=True, show_default=True, default=False, help="Format the file after adding the docstrings.")
@click.argument('path', type=click.Path(exists=True))
def run(mode, path, format):
    """
    Automatically adds docstrings to Python files in the given PROJECT_FOLDER.
    """

    config = Config()
    config.load()
    logging.info(config.settings)
    assistant_id = config.settings.get('ASSISTANT_ID')
    assistant_instructions = config.settings.get('ASSISTANT_INSTRUCTIONS')
    prompt = config.settings.get('AI_PROMPT')
    if not assistant_instructions:
        logging.error("ASSISTANT_INSTRUCTIONS is required. have you ran `autodoc configure`?")
        exit(1)
    if not prompt:
        logging.error("PROMPT is required. have you ran `autodoc configure`?")
        exit(1)
    if not os.getenv('OPENAI_API_KEY'):
        logging.error("PROMPT is required. have you ran `autodoc configure`?")
        exit(1)

    auto_doc = AIAutodocService(
        assistant_id=assistant_id,
        assistant_instructions=assistant_instructions,
        prompt=prompt
    )
    if not assistant_id:
        logging.info('Persisting your assistance id into your config file...')
        config.settings['ASSISTANT_ID'] = auto_doc.get_assistant_id()
        config.persist_settings()

    runner = Runner(autodoc_service=auto_doc, auto_format=format)

    if mode == 'folder':
        runner.run_for_folder(folder_path=path)
    elif mode == 'file':
        runner.run_for_file(file_path=path)
    else:
        click.echo("Invalid mode specified. Use 'folder' or 'file'.")


@click.command()
def configure():
    config = Config()
    config.initialize()


cli.add_command(run)
cli.add_command(configure)
