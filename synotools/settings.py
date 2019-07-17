import os
from os.path import join
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def get_environmental_variable(var_name: str) -> Optional[str]:
    """Simple wrapper method that guarantees dotenv load"""
    return os.getenv(var_name, None)


def get_local_credentials_path():
    return join(str(Path.home()), ".synotools/credentials")


load_dotenv(dotenv_path=get_local_credentials_path(), verbose=True)
