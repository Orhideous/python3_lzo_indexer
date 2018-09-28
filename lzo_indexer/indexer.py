import struct
from typing import BinaryIO, NamedTuple

# Magic string expected at the start of the file to verify it's LZO
LZO_MAGIC = bytearray([0x89, 0x4c, 0x5a, 0x4f, 0x00, 0x0d, 0x0a, 0x1a, 0x0a])
SUFFIXES = frozenset({".lzo", ".lzop"})

_COMPRESSION_CHECKSUMS = (0x02, 0x200)  # ADLER32 CRC32
_DECOMPRESSION_CHECKSUMS = (0x01, 0x100)  # ADLER32 CRC32

F_H_EXTRA_FIELD = 0x00000040


class Checksums(NamedTuple):
    compressed: int
    decompressed: int


def _parse_header(lzo_file: BinaryIO) -> Checksums:
    """
    Parse and verify the header of an LZO file, returning a tuple
    of the number of compressed/decompressed checksums expected at the
    end of each block.
    """

    if lzo_file.tell() != 0:
        raise Exception("File object must be at offset 0")

    # Parse the header
    if lzo_file.read(9) != LZO_MAGIC:
        raise Exception("Invalid lzo file")

    # Ignore a bunch of values from the header
    # TODO: We should validate these
    lzo_file.read(2)  # lzop_version
    lzo_file.read(2)  # library_version
    lzo_file.read(2)  # extract_version
    lzo_file.read(1)  # method
    lzo_file.read(1)  # level

    # Checksum flags
    flags, = struct.unpack(">I", lzo_file.read(4))

    num_compressed_checksums = 0
    for idx, flag in enumerate(_COMPRESSION_CHECKSUMS):
        if (flag & flags) != 0:
            num_compressed_checksums += 1

    num_decompressed_checksums = 0
    for idx, flag in enumerate(_DECOMPRESSION_CHECKSUMS):
        if (flag & flags) != 0:
            num_decompressed_checksums += 1

    # Parse out the mode/mtime/gmtdiff values we're not interested in
    lzo_file.read(4)  # mode
    lzo_file.read(4)  # mtime
    lzo_file.read(4)  # gmtdiff

    # Extract the filename
    filename_length = ord(lzo_file.read(1))
    if filename_length > 0:
        str(lzo_file.read(filename_length))  # filename

    # TODO: Verify the header checksum against these bytes
    lzo_file.read(4)

    # Process extra header field for lzo < 1.08. This is a checksum that
    # needs to also be validated
    if (flags & F_H_EXTRA_FIELD) != 0:
        size, = struct.unpack(">I", lzo_file.read(4))
        if size > 0:
            lzo_file.read(size)
        lzo_file.read(4)

    return Checksums(
        compressed=num_compressed_checksums,
        decompressed=num_decompressed_checksums
    )


def get_lzo_blocks(lzo_file: BinaryIO):
    """
    Return a generator containing all of the block offsets for each
    compressed block of data in the LZO file.
    """

    checksums = _parse_header(lzo_file)

    while True:
        decompressed_blocksize, = struct.unpack(">I", lzo_file.read(4))
        if decompressed_blocksize == 0:
            break

        compressed_blocksize, = struct.unpack(">I", lzo_file.read(4))

        checksums_to_skip = checksums.decompressed
        if decompressed_blocksize == compressed_blocksize:
            checksums_to_skip += checksums.compressed

        skip = 4 * checksums_to_skip

        position = lzo_file.tell()

        block_start = position - 8  # Rewind back to before the block headers
        next_block = position + compressed_blocksize + skip

        yield block_start

        lzo_file.seek(next_block)  # Seek to the next block


def index_lzo_file(lzo_file: BinaryIO, index_file: BinaryIO):
    """
    Index the given LZO stream and write the index to the given output stream
    """
    for block in get_lzo_blocks(lzo_file):
        index_file.write(struct.pack(">Q", block))
