from cacheusagesimulator.file_generator import BlockFileGenerator

# Horrible singleton...
_block_file_generator = BlockFileGenerator()


def block_next_get() -> bytearray:
    return _block_file_generator.create_random_file()
