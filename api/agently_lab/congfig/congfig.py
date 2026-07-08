import os
from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from agently import Agently, AgentlyMain

if TYPE_CHECKING:
    from agently import AgentlyMain

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

config_file = Path(__file__).parent / "llm_config.yaml"

def _resolve_auth(key_ref: str | None) -> str | None:
    if not key_ref:
        return None
    if key_ref.startswith("$"):
        return os.getenv(key_ref[1:])
    return key_ref


def init_agently(agently_instant: "AgentlyMain", mode_name: str = "siliconflow-ds"):
    with open(config_file) as file:
        settings = yaml.safe_load(file)
        models_settings = settings.get(mode_name)
    base_url = models_settings.get("base_url")
    model_name = models_settings.get("model")
    key_ref = models_settings.get("api_key")
    agently_instant.set_settings(
        "OpenAICompatible",
        {
            "base_url": base_url,
            "model": model_name,
            "auth": _resolve_auth(key_ref),
        },
    )

    

if __name__ == "__main__":
    init_agently(Agently)
