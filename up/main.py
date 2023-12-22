from sys import argv as args
from datetime import datetime

from up import cli
from up.logging import log
from up.config.file import setup_container
from up.config.container import DockerContainer

def print_help():
    log.debug("up [prompt]")


def exit_cli(code=-1):
    if code:
        log.error("Exiting up cli with code %s", code)
    sys.exit(code)


def cli_main():
    now = datetime.now()
    log.info(f"Starting UP cli at {now.isoformat()}")
    len_args = len(args)
    if len_args < 1:
        print_help()
        exit_cli("NO_COMMAND_SPECIFIED")
    executable = args[0]
    prompt = args[1:]
    if cli.keyword_in_prompt(prompt):
        cli.run_keyword(prompt)
    context = {"executable": executable}
    try:
        config = setup_container(prompt)
        container = DockerContainer()
        container.run(config)
        #uplib.up_main(context, prompt)
    except Exception as e:
        log.error(e)
        # print stack trace
        raise e
        exit_cli("UP_ERROR")
        
