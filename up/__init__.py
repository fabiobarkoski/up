import os
from pathlib import Path
from ruamel.yaml import YAML

home = os.path.expanduser("~")
up_dir = Path(home, '.up')
yaml = YAML()
