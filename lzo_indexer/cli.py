from functools import partial
from typing import List

from multiprocessing import cpu_count
from multiprocessing import Pool

import click
from pathlib import Path

from lzo_indexer import index_lzo_file
from lzo_indexer.indexer import SUFFIXES


def indexer(*, force: bool, extension: str, file_name: str) -> bool:
    archive = Path(file_name)
    archive_index = archive.with_suffix(archive.suffix + extension)

    if archive.suffix not in SUFFIXES:
        click.echo(click.style(f"File {file_name} seems like not LZO archive, skip it", fg="yellow", bold=True))
        return False

    if archive_index.exists() and not force:
        click.echo(click.style(f"Index for {file_name} already exists", fg="yellow", bold=True))
        return False

    with archive.open(mode="rb") as f_in, archive_index.open(mode="wb") as f_out:
        index_lzo_file(f_in, f_out)

    click.echo(f"Created index for {click.style(file_name, bold=True)}")

    return True


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--threads", "-t",
    expose_value=True, type=int, default=cpu_count(),
    help="Processing threads count"
)
@click.option(
    "--extension", "-e",
    expose_value=True, type=str, default=".index",
    help="Index file extension"
)
@click.option(
    "--force", "-f",
    is_flag=True, expose_value=True, default=False,
    help="Force re-creation of an index even if it exists"
)
@click.argument(
    "files",
    required=True, type=click.Path(exists=True, dir_okay=False), nargs=-1,
    metavar="<files to index>"
)
def cli(files: List[str], force: bool, extension: str, threads: int):
    """Tool for indexing LZO compressed files"""
    with Pool(processes=threads) as pool:
        indexed = sum(pool.map(partial(indexer, force, extension), files))

    if indexed:
        click.echo(click.style(f"Successfully indexed {indexed} files", fg="green", bold=True))
