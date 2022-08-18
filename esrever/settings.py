import os
import pathlib
import typing
import glob

from pydantic import BaseSettings, Field, validator

GHIDRA_HEADLESS_LOCATION ="/support/analyzeHeadless"
GHIDRA_SEARCH_PATHS: typing.List[str] = [
    '~/ghidra*',
    '~/opt/ghidra*',
    '/opt/ghidra*',
]


def _expand_path(path: str) -> str:
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    return path


def _find_matching_pattern(path_patterns: typing.List[str], prefix: str = '', suffix: str = '') -> typing.Optional[str]:
    for path_pattern in path_patterns:
        full_pattern = f"{prefix}{path_pattern}{suffix}"
        full_pattern = _expand_path(full_pattern)
        if results := list(glob.glob(full_pattern)):
            return results[0].replace(suffix, '')


def find_installed_ghidra() -> typing.Optional[str]:
    return _find_matching_pattern(GHIDRA_SEARCH_PATHS, suffix=GHIDRA_HEADLESS_LOCATION)


class EsreverSettings(BaseSettings):

    ghidra_path: pathlib.Path = Field(default_factory=find_installed_ghidra)

    @validator("ghidra_path", pre=True, always=True)
    def validate_ghidra_path(cls, v):
        if not v:
            v = find_installed_ghidra()
        return v

    @property
    def ghidra_headless_path(self):
        return f"{self.ghidra_path}{GHIDRA_HEADLESS_LOCATION}"
