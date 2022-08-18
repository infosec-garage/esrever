import os
import pathlib
import typing
import glob
import click
import subprocess
from tqdm.cli import tqdm

from .settings import EsreverSettings
from .data import DATA_DIR

class GlobPath(click.ParamType):

    name = "Path or glob pattern representing multiple files."

    CONVERTED_SINGLE_TYPE = typing.List[pathlib.Path]
    CONVERTED_MULTIPLE_TYPE = typing.Tuple[CONVERTED_SINGLE_TYPE]

    def convert(
        self, value: typing.Any, param: typing.Optional[click.Parameter], ctx: typing.Optional[click.Context]
    ) -> typing.List[pathlib.Path]:
        glob_value = glob.glob(str(value))
        return [pathlib.Path(glob_match) for glob_match in glob_value]

    @staticmethod
    def combine(values: typing.Tuple[typing.List[pathlib.Path]]) -> typing.Set[pathlib.Path]:
        result_set: typing.Set[pathlib.Path] = set()
        for value in values:
            if isinstance(value, pathlib.Path):
                result_set.add(value)
            elif isinstance(value, list):
                for sub_value in value:
                    if isinstance(sub_value, pathlib.Path):
                        result_set.add(sub_value)
        return result_set







config = click.option(
    "config",
    "--config",
    "-c")
output_dir = click.option(
    "output_dir",
    "--output-dir",
    "-o",
    type=click.Path(
        dir_okay=True,
        file_okay=False))
input_files = click.argument(
    "input_files",
    type=GlobPath(),
    required=True,
    nargs=-1,
)


def decompile(settings: EsreverSettings, input_file: pathlib.Path, output_file: pathlib.Path):

    # echo time $GHIDRA_PATH/support/analyzeHeadless . tmp_ghidra_project -import $1  -postscript $DECOMPILE_SCRIPT_PATH/Decompile.java $2
    subprocess.run(
        [
            settings.ghidra_headless_path,
            ".",
            "tmp_ghidra_project",
            "-scriptPath",
            DATA_DIR,
            "-import",
            str(input_file.absolute()),
            "-postscript",
            f"{DATA_DIR}/Decompile.java",
            str(output_file.absolute())
            ]
    )



@click.group("esrever")
def cli_app():
    ...

@cli_app.command("decompile")
@config
@input_files
def decompile_command(
        input_files: typing.List[pathlib.Path],
        config: typing.Optional[str] = None,
        output_dir: typing.Optional[pathlib.Path] = None):
    """Reverse a set of binary files with Ghidra."""
    config = config or EsreverSettings()
    input_files = GlobPath.combine(input_files)
    output_dir = output_dir or pathlib.Path(os.getcwd()).joinpath("out")
    if not output_dir.exists():
        output_dir.mkdir()
    for input_file in tqdm(input_files):
        output_file = output_dir.joinpath(f"{input_file.stem}.c")
        decompile(settings=config, input_file=input_file, output_file=output_file)

