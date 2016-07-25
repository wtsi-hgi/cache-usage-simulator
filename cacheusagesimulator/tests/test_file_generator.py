import unittest

from cacheusagesimulator.file_generator import BlockFileGenerator


class TestBlockFileGenerator(unittest.TestCase):
    def setUp(self):
        self.bytes_per_block = 1024
        self.mean_blocks_per_file = 42
        self.blocks_per_file_spread = 0
        self.file_generator = BlockFileGenerator(bytes_per_block=self.bytes_per_block,
                                                 mean_blocks_per_file=self.mean_blocks_per_file,
                                                 blocks_per_file_spread=self.blocks_per_file_spread)

    def test_create_random_file(self):
        file = self.file_generator.create_random_file()
        self.assertEqual(self.mean_blocks_per_file, len(file.block_hashes))

    def test_create_random_block(self):
        self.assertEqual(self.bytes_per_block, len(self.file_generator._create_random_block()))


if __name__ == "__main__":
    unittest.main()
