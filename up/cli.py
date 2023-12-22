import os
import requests
from pathlib import Path

from up.logging import log
from up import home, up_dir, yaml

def init():
    log.info('Initializing up...')
    if os.path.exists(up_dir):
        log.info('seems that up is already initialized')
        return
    log.info('Creating UP dir')
    os.mkdir(up_dir)
    default_config = input('use default config?[y/n] ')
    while default_config != 'y' and default_config != 'n':
        default_config = input('use default config?[y/n] ')
    if default_config == 'y':
        with open(Path(up_dir, 'up.yaml'), 'w') as file:
            yaml.dump({'default_image': 'fedora'}, file)
    log.info('init ended :)')

def add(prompt):
    log.info('downloading...')
    r = requests.get(prompt[2])
    with open(Path(up_dir, prompt[1]), 'wb') as file:
        file.write(r.content)
    log.info('download ended')

def remove():
    print('remove')

_reserved_keywords = {
    "init": init,
    "add": add,
    "remove": remove,
}

def keyword_in_prompt(prompt: list[str]) -> bool:
    kw = prompt[0]
    match kw:
        case kw if kw in _reserved_keywords.keys():
            return True
        case _:
            return False

def run_keyword(prompt: list[str]):
    _reserved_keywords[prompt[0]](prompt)
    exit(0)
