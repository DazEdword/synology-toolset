import os

from constants import ENV_PATH
from dotenv import load_dotenv
from typing import Optional

load_dotenv(dotenv_path=ENV_PATH, verbose=True)


def get_environmental_variable(var_name: str) -> Optional[str]:
    """Simple wrapper method that guarantees load_dotenv"""
    return os.getenv(var_name, None)
