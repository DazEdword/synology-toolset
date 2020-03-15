import os
import sys
from os.path import join
from pathlib import Path

from dotenv import load_dotenv


class Settings:
    def __init__(self):
        load_dotenv(dotenv_path=self.credentials_path, verbose=True)

    @property
    def credentials_path(self):
        if sys.platform.startswith("win"):
            CREDENTIALS_PATH = ".synotools\\credentials.txt"
        else:
            CREDENTIALS_PATH = ".synotools/credentials"

        return join(str(Path.home()), CREDENTIALS_PATH)

    def get_environmental_variable(self, var_name):
        """Simple wrapper method that guarantees dotenv load"""
        return os.getenv(var_name, None)
