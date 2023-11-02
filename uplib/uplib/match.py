import logging as log
from . import Prompt
from typing import Callable
from .containers import ContainerRun


def does_match(prompt: Prompt, args) -> bool:
    for p, a in zip(prompt, args):
        if p != a:
            return False
    return True


def if_prompt_matches(mk_run_config: Callable[[], ContainerRun],
                 prompt: Prompt,
                 *args) -> list[ContainerRun]:
    if not prompt:
        return None
    if does_match(prompt, args):
        log.info(f"MATCH: prompt={prompt}, args={args}")
        return [mk_run_config(prompt)]
    log.info(f"NO MATCH: prompt={prompt}, args={args}")
    return None