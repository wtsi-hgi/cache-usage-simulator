from math import ceil
from typing import List, Optional

from cacheanalysis.models import BlockFile
from records import Record

from cacheusagesimulator.file_generator import BlockFileGenerator


class UsageGenerator():
    """
    Generates simulated records indicating the usage of a cache.
    """
    def __init__(self, file_generator: BlockFileGenerator,
                 average_proportion_of_blocks_read_when_sequential_read: int=None,
                 average_block_reads_between_reference_read: int=None,
                 average_proportion_of_block_reads_on_reference_access: int=None,
                 known_file_read_probability: float=None):
        """
        Constructor.
        :param file_generator: the block file generator
        :param average_proportion_of_blocks_read_when_sequential_read: the average proportion of all blocks in a file
        that are read sequentially upon first access to the file. If 0.5, on average (using some distribution and some
        measure of average), half of a file's blocks will be read sequentially when it is accessed
        :param average_block_reads_between_reference_read: the average number of block reads between reading a number of
        blocks from a reference file (using some distribution and some measure of average)
        :param average_proportion_of_block_reads_on_reference_access: the average proportion of blocks read from the
        reference when it is accessed (using some distribution and some measure of average)
        :param known_file_read_probability: the probability that a non-reference file that has been read before will be
        read again
        """
        self.average_proportion_of_blocks_read_when_sequential_read = average_proportion_of_blocks_read_when_sequential_read \
            if average_proportion_of_blocks_read_when_sequential_read is not None \
            else ceil(file_generator.mean_blocks_per_file / 2)
        self.mean_block_reads_between_reference_block_read = average_block_reads_between_reference_read \
            if average_block_reads_between_reference_read is not None \
            else file_generator.mean_blocks_per_file * 25
        self.average_proportion_of_block_reads_on_reference_access = average_proportion_of_block_reads_on_reference_access \
            if average_proportion_of_block_reads_on_reference_access is not None \
            else 1.0
        self.known_file_read_probability = known_file_read_probability\
            if known_file_read_probability is not None \
            else 0.1

        # Note: You will probably need internal variables such as these - please feel free to change them though!
        self._known_reference_files = []  # type: List[BlockFile]
        self._known_non_reference_files = []
        self._blocks_in_cache = []     # type: List[str]
        self._current_file = None   # type: Optional[BlockFile]
        self._current_file_index = 0

    def generate(self) -> Record:
        """
        Randomly generates the next record to simulate usage of a cache.
        :return: the next record
        """
        # TODO
