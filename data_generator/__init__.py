"""Top-level package exports for the template package.

Overview:
- Purpose: Define what the package exposes as public API.
- Used by: Python import system and downstream users.
- Adds: Stable import paths and cleaner user-facing package surface.
- Learn more: https://docs.python.org/3/tutorial/modules.html#packages
"""

from importlib.metadata import PackageNotFoundError, version

from . import generate_dataset as _api
from .generate_dataset import *  # noqa: F401,F403

__all__ = list(_api.__all__)

try:
    __version__ = version("data_generator")
except PackageNotFoundError:
    __version__ = "0.0.0"
