from shlex import join
from pathlib import Path
from dynaconf import Dynaconf
from dataclasses import dataclass, field

from up import up_dir
from up.logging import log
from up.config.container import ContainerRun

@dataclass
class SettedPrompt:
    image: str = field(kw_only=True, default="")
    command: str  = field(kw_only=True, default="")
    environment: dict[str, str]  = field(kw_only=True, default_factory=dict)
    ports: dict[str, str]  = field(kw_only=True, default_factory=dict)
    volumes: dict[str, str]  = field(kw_only=True, default_factory=dict)

def setup_container(prompt: list[str]) -> ContainerRun:
    filename = list(up_dir.glob(prompt[0]+'.yaml'))
    if not filename:
        filename = default_file()
    settings = Dynaconf(
        load_dotenv=True,
        envvar_prefix="UP_",
        settings_file=Path(up_dir, filename[0])
    )

    command = join(prompt)
    prompts = [p['prompt'] for p in settings.get('prompts', [])]
    if command in prompts:
        return load_prompt(prompts.index(command), settings)

    return ContainerRun(
        image=settings.get('image'),
        command=command,
        volumes=settings.get('volumes', {}),
        ports=settings.get('ports', {}),
    )

def default_file() -> list[str]:
    log.info('File not found, using the default config from up')
    return ['up.yaml']

def load_prompt(prompt_index: int, settings: Dynaconf) -> ContainerRun:
    command = settings['prompts'][prompt_index].get('prompt')
    if 'alias' in settings['prompts'][prompt_index].keys():
        command = settings['prompts'][prompt_index].get('alias')
    prompt_values = SettedPrompt(
        command=command,
        environment=settings['prompts'][prompt_index].get('env', {}),
        volumes=settings['prompts'][prompt_index].get('volumes', {}),
        ports=settings['prompts'][prompt_index].get('ports', {})
    )
    
    return ContainerRun(
        image=settings.get('image'),
        command=prompt_values.command if prompt_values.command else prompt,
        volumes=settings.get('volumes', {}) | prompt_values.volumes,
        ports=settings.get('ports', {}) | prompt_values.ports,
    )
