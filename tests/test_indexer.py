from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from lzo_indexer.indexer import get_lzo_blocks
from lzo_indexer.cli import indexer


def test_get_blocks_single_block(small_lzo):
    index = get_lzo_blocks(small_lzo)

    block = next(index)
    assert block == 38
    with pytest.raises(StopIteration):
        next(index)


def test_get_blocks_multiple_blocks(big_lzo):
    index = get_lzo_blocks(big_lzo)

    expected_offsets = [38, 1233, 2428, 3623]
    assert expected_offsets == list(index)


def test_index_lzo_file_single_block(small_lzo):
    with NamedTemporaryFile(suffix=".lzo") as temp:
        extension = ".index"
        archive = Path(temp.name)
        archive_index = archive.with_suffix(archive.suffix + extension)
        with archive.open(mode="wb") as f:
            f.write(small_lzo.read())

        indexer(force=False, extension=extension, file_name=archive.as_posix())

        assert archive_index.exists()
        assert archive_index.read_bytes() == bytearray([
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x26
        ])
        archive_index.unlink()


def test_skip_existing_index(small_lzo):
    with NamedTemporaryFile(suffix=".lzo") as temp:
        extension = ".index"
        archive = Path(temp.name)
        archive_index = archive.with_suffix(archive.suffix + extension)
        archive_index.write_bytes(b'\x00')
        with archive.open(mode="wb") as f:
            f.write(small_lzo.read())

        indexer(force=False, extension=extension, file_name=archive.as_posix())

        assert archive_index.exists()
        assert archive_index.read_bytes() == bytearray([0x0])
        archive_index.unlink()


def test_force_overwrite_existing_index(small_lzo):
    with NamedTemporaryFile(suffix=".lzo") as temp:
        extension = ".index"
        archive = Path(temp.name)
        archive_index = archive.with_suffix(archive.suffix + extension)
        archive_index.write_bytes(b'\x00')
        with archive.open(mode="wb") as f:
            f.write(small_lzo.read())

        indexer(force=True, extension=extension, file_name=archive.as_posix())

        assert archive_index.exists()
        assert archive_index.read_bytes() != bytearray([0x0])
        assert archive_index.read_bytes() == bytearray([
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x26
        ])
        archive_index.unlink()


def test_index_lzo_file_multiple_blocks(big_lzo):
    with NamedTemporaryFile(suffix=".lzo") as temp:
        extension = ".index"
        archive = Path(temp.name)
        archive_index = archive.with_suffix(archive.suffix + extension)
        with archive.open(mode="wb") as f:
            f.write(big_lzo.read())

        indexer(force=False, extension=extension, file_name=archive.as_posix())

        assert archive_index.exists()
        assert archive_index.read_bytes() == bytearray([
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x26,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4, 0xd1,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x9, 0x7c,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xe, 0x27
        ])
        archive_index.unlink()
