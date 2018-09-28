from io import BytesIO
from subprocess import Popen, PIPE

import pytest


def lzo_stream(*, length: int = 4096):
    """
    Compress a string of null bytes, the length being defined by the
    argument to this function.
    """

    compressor = Popen(["lzop", "-c"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = compressor.communicate(input=b"\x00" * length)

    if stderr:
        raise Exception(f"Failed to compress with error {stderr!r}")

    stream = BytesIO(stdout)
    stream.seek(0)

    return stream


@pytest.fixture
def small_lzo():
    return lzo_stream(length=1)


@pytest.fixture
def big_lzo():
    return lzo_stream(length=10 ** 6)
