import os
from os.path import join
from pathlib import Path

from dotenv import load_dotenv

CREDENTIALS_PATH = ".synotools/credentials"


class Settings:
    def __init__(self):
        load_dotenv(dotenv_path=self.get_local_credentials_path, verbose=True)

    @property
    def get_local_credentials_path(self):
        return join(str(Path.home()), CREDENTIALS_PATH)

    def get_environmental_variable(self, var_name):
        """Simple wrapper method that guarantees dotenv load"""
        return os.getenv(var_name, None)
