import random

from cacheanalysis.models import BlockFile
from math import ceil

from cacheusagesimulator._common import DEFAULT_BLOCKS_PER_FILE, DEFAULT_BLOCK_SIZE, \
    DEFAULT_BLOCKS_PER_FILE_SPREAD


def md5() -> str:
    return "{:032x}".format(random.getrandbits(128))


class BlockFileGenerator:
    """
    Generates block files.
    """
    def __init__(self, bytes_per_block: int=DEFAULT_BLOCK_SIZE,
                 mean_blocks_per_file: int=DEFAULT_BLOCKS_PER_FILE,
                 blocks_per_file_spread: int=DEFAULT_BLOCKS_PER_FILE_SPREAD):
        """
        Constructor.
        :param bytes_per_block: the total number of bytes in a block (must be >0)
        :param mean_blocks_per_file: the mean number of blocks in a file (must be >0)
        :param blocks_per_file_spread: the spread in a normal distribution for the number of blocks
        in a file (should be <(mean_blocks_per_file/3) - having it higher than
        that is likely to cause files of 0 length to be generated)
        """
        self.bytes_per_block = bytes_per_block
        self.mean_blocks_per_file = mean_blocks_per_file
        self.blocks_per_file_spread = blocks_per_file_spread

    def create_random_file(self) -> BlockFile:
        """
        Creates a file made from a random number of random blocks, with a random name.
        :return: the generated file
        """
        return BlockFile(
            md5(),
            [md5() for _ in range(ceil(
                random.gauss(self.mean_blocks_per_file,
                             self.blocks_per_file_spread if self.blocks_per_file_spread >= 0 else 0
                )
            ))]
        )

    def _create_random_block(self) -> bytearray:
        """
        Creates a random block of bytes.
        :return: the generated block
        """
        return bytearray(random.getrandbits(8) for _ in range(self.bytes_per_block))
