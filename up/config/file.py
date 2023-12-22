from pathlib import Path
from shlex import join

from up.logging import log
from up import home, up_dir, yaml
from up.config.container import ContainerRun

def setup_container(prompt: list[str]):
    file = list(up_dir.glob(prompt[0]+'.yaml'))
    if not file:
        raise Exception("File not found")
    with open(Path(up_dir, file[0]), 'r') as f:
        file_values = yaml.load(f)

    result = ContainerRun(
        image=file_values['image'],
        command='echo oie',
        volumes=file_values['volumes'],
        ports=file_values['ports']
    )

    return result

