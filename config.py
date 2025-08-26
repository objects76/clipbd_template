

from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass
class Config:
    clipbd_transcript: bool = False
    clear_generated: bool = False

    def __init__(self, config_path: str):
        template_yaml = Path(config_path).expanduser()
        if not template_yaml.exists():
            raise ValueError(f'not found: {template_yaml}')

        config = yaml.safe_load(template_yaml.read_text(encoding='utf-8')) or {}
        config = config.get('config', {})
        Config.clipbd_transcript = config.get('clipbd_transcript', Config.clipbd_transcript)
        Config.clear_generated = config.get('clear_generated', Config.clear_generated)



if __name__ == '__main__':
    # config = Config('~/.config/rofi/template.yaml')

    print(Config.clipbd_transcript)
    print(Config.clear_generated)