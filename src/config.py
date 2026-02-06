from dataclasses import dataclass
from pathlib import Path

import yaml

from exceptions import ConfigurationError


@dataclass
class Config:
    clipbd_transcript: bool = False
    clear_generated: bool = False

    webai: str = "https://www.chatgpt.com"
    browser_profile: str = "Default"
    webai_title: str = "chatgpt"

    # webai: str = "https://gemini.google.com/app"
    # browser_profile: str = "Profile 2"
    # webai_title: str = "gemini"

    markdown_editor: str = "mdviewer.app"
    use_api: bool = False

    def __init__(self, config_path: str):
        template_yaml = Path(config_path).expanduser()
        if not template_yaml.exists():
            raise ConfigurationError(f"Configuration file not found: {template_yaml}")

        config = yaml.safe_load(template_yaml.read_text(encoding="utf-8")) or {}
        config = config.get("config", {})
        Config.clipbd_transcript = config.get(
            "clipbd_transcript", Config.clipbd_transcript
        )
        Config.clear_generated = config.get("clear_generated", Config.clear_generated)

        Config.webai = config.get("webai", Config.webai)
        Config.browser_profile = config.get("browser_profile", Config.browser_profile)
        Config.webai_title = config.get("webai_title", Config.webai_title)

        Config.markdown_editor = config.get("markdown_editor", Config.markdown_editor)
        Config.use_api = config.get("use_api", Config.use_api)


if __name__ == "__main__":
    config = Config("asset/template2.yaml")
    print(f"clipbd_transcript: {Config.clipbd_transcript}")
    print(f"clear_generated: {Config.clear_generated}")

    print(f"markdown_editor: {Config.markdown_editor}")
    print(f"use_api: {Config.use_api}")

    print(f"webai: {Config.webai}")
    print(f"browser_profile: {Config.browser_profile}")
    print(f"webai_title: {Config.webai_title}")
