from datetime import datetime, timedelta
from math import ceil
import random
from typing import List, Optional, Generator

from cacheanalysis.models import BlockFile
from cacheanalysis.models import Record, CacheMissRecord, CacheHitRecord, CacheDeleteRecord

from cacheusagesimulator.file_generator import BlockFileGenerator


class UsageGenerator:
    """
    Generates simulated records indicating the usage of a cache.
    """

    def __init__(self, file_generator: BlockFileGenerator = BlockFileGenerator(),
                 average_proportion_of_blocks_read_when_sequential_read: float = 0.5,
                 average_block_reads_between_reference_read: float = None,
                 average_proportion_of_block_reads_on_reference_access: float = 1.0,
                 known_file_reread_probability: float = 0.1,
                 number_of_files: int = 40,
                 probability_file_is_reference: float = 0.1,
                 max_cache_size: int = 1000):
        """
        Constructor.
        :param file_generator: the block file generator
        :param average_proportion_of_blocks_read_when_sequential_read: the average proportion of all blocks in a file
        that are read sequentially upon first access to the file. If 0.5, on average (using some distribution and some
        measure of average), half of a file's blocks will be read sequentially when it is accessed
        :param average_block_reads_between_reference_read: the average number of block reads between reading from a
        reference file (using some distribution and some measure of average)
        :param average_proportion_of_block_reads_on_reference_access: the average proportion of blocks read from the
        reference when it is accessed (using some distribution and some measure of average)
        :param known_file_reread_probability: the probability that a non-reference file that has been read before will be
        read again
        :param number_of_files: the number of files to generate
        :param probability_file_is_reference: the probability a file is a reference file
        :param max_cache_size: the maximum cache size in blocks
        """
        self.average_proportion_of_blocks_read_when_sequential_read = average_proportion_of_blocks_read_when_sequential_read
        self.average_block_reads_between_reference_block_read = average_block_reads_between_reference_read \
            if average_block_reads_between_reference_read is not None \
            else file_generator.mean_blocks_per_file * 25
        self.average_proportion_of_block_reads_on_reference_access = average_proportion_of_block_reads_on_reference_access
        self.known_file_reread_probability = known_file_reread_probability
        self.number_of_files = number_of_files
        self.probability_file_is_reference = probability_file_is_reference
        self.max_cache_size = max_cache_size

        self.known_reference_files = []  # type: List[BlockFile]
        self.known_non_reference_files = []  # type: List[BlockFile]

        # Note: You will probably need internal variables such as these - please feel free to change them though!
        self._file_generator = BlockFileGenerator()
        self._unknown_files = []  # type: List[BlockFile]
        self._blocks_in_cache = []  # type: List[str]
        self._current_file = None  # type: Optional[BlockFile]
        self._current_file_index = 0
        self._blocks_to_read = 0
        self._total_blocks_read = 0
        for i in range(self.number_of_files):
            self._unknown_files.append(self._file_generator.create_random_file())
        if False:
            if random.random() < self.probability_file_is_reference:
                self.known_reference_files.append(self._file_generator.create_random_file())
            else:
                self.known_non_reference_files.append(self._file_generator.create_random_file())
        self._time = datetime(year=2000, month=1, day=1)

        self._generator = self._create_generator()

    def generate(self) -> Record:
        """
        Randomly generates the next record to simulate usage of a cache.
        :return: the next record
        """
        return next(self._generator)

    def _create_generator(self) -> Generator:
        # pick random file to read from
        #   if probability_file_is_reference or average_block_reads_between_reference_read has passed, make it a reference
        # pick random number of blocks to read
        #   average_proportion_of_blocks_read_when_sequential_read on first (sequential) read
        # pick random place in file to read from
        #   must allow reading the (predetermined) number of blocks to read
        # for each block:
        # if in cache, CacheHitRecord
        #   otherwise:
        #     if free space in cache, CacheMissRecord
        #     otherwise:
        #       CacheDeleteRecord for other block
        #       CacheMissRecord for new block
        while True:
            if self._blocks_to_read <= 0:
                # finished reading a file
                if random.random() < self.probability_file_is_reference or self._total_blocks_read >= self.average_block_reads_between_reference_block_read:
                    # read a reference file
                    if len(self._unknown_files) > 0:
                        # still files that haven't been read, read one of them next
                        self._current_file = self._unknown_files.pop()
                        self.known_reference_files.append(self._current_file)
                    else:
                        # all files have been read, pick a random file to read next
                        self._current_file = random.choice(self.known_reference_files)
                else:
                    # read a non-reference file
                    if random.random() > self.known_file_reread_probability and len(self._unknown_files) > 0:
                        # we should not reread a known file
                        self.known_non_reference_files.append(self._unknown_files.pop())
                        self._current_file = self.known_non_reference_files[-1]
                    else:
                        # we should read an existing file (maybe there are no unknown files left)
                        self._current_file = random.choice(self.known_non_reference_files)
                while True:
                    self._blocks_to_read = ceil(
                        len(self._current_file.block_hashes) * random.gauss(
                            self.average_proportion_of_blocks_read_when_sequential_read,
                            self.average_proportion_of_blocks_read_when_sequential_read / 4
                        )
                    )
                    try:
                        self._current_file_index = random.randrange(
                            len(self._current_file.block_hashes)
                            - self._blocks_to_read)
                    except ValueError:
                        # argument to random.randrange == 0, so we must start reading at the start of the file
                        self._current_file_index = 0
                    if self._blocks_to_read + self._current_file_index >= len(self._current_file.block_hashes):
                        continue
                    else:
                        break
            while self._blocks_to_read > 0:
                self._time += timedelta(days=1)
                if self._current_file.block_hashes[self._current_file_index] in self._blocks_in_cache:
                    # block is in cache
                    self._blocks_to_read -= 1
                    self._current_file_index += 1
                    self._total_blocks_read += 1
                    yield CacheHitRecord(
                        self._current_file.block_hashes[self._current_file_index - 1],
                        self._time)
                else:
                    # block is not in cache
                    if len(self._blocks_in_cache) >= self.max_cache_size:
                        # cache too big, remove a random block from it
                        yield CacheDeleteRecord(self._blocks_in_cache.pop(
                            random.randrange(len(self._blocks_in_cache))), self._time)
                    self._blocks_in_cache.append(
                        self._current_file.block_hashes[self._current_file_index])
                    self._blocks_to_read -= 1
                    self._current_file_index += 1
                    self._total_blocks_read += 1
                    yield CacheMissRecord(
                        self._current_file.block_hashes[self._current_file_index - 1],
                        self._time,
                        64 * 1024 ** 2  # 64 MB
                    )
