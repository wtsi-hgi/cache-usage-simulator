from cacheanalysis.models import BlockFile

from cacheusagesimulator._common import DEFAULT_BLOCK_SIZE, \
    DEFAULT_BLOCKS_PER_FILE


class BlockFileGenerator:
    """
    Generates block files.
    """
    def __init__(self, bytes_per_block: int=DEFAULT_BLOCK_SIZE, mean_blocks_per_file: int=DEFAULT_BLOCKS_PER_FILE):
        """
        Constructor.
        :param bytes_per_block: the total number of bytes in a block (must be >0)
        :param mean_blocks_per_file: the mean number of blocks in a file (must be >0)
        """
        self.bytes_per_block = bytes_per_block
        self.mean_blocks_per_file = mean_blocks_per_file

    def create_random_file(self) -> BlockFile:
        """
        Creates a file made from a random number of random blocks, with a random name.
        :return: the generated file
        """

    def _create_random_block(self) -> bytearray:
        """
        Creates a random block of bytes.
        :return: the generated block
        """
