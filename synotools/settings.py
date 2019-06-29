import os

from dotenv import load_dotenv
from typing import Optional

from synotools.constants import ENV_PATH


load_dotenv(dotenv_path=ENV_PATH, verbose=True)


def get_environmental_variable(var_name: str) -> Optional[str]:
    """Simple wrapper method that guarantees dotenv load"""
    return os.getenv(var_name, None)
