from cacheanalysis.models import BlockFile
from hgijson import MappingJSONEncoderClassBuilder, JsonPropertyMapping

from cacheusagesimulator.file_generator import BlockFileGenerator

_block_file_generator = BlockFileGenerator(blocks_per_file_spread=0)


BlockFileJSONEncoder = MappingJSONEncoderClassBuilder(
    BlockFile,
    [
        JsonPropertyMapping("name", "name"),
        JsonPropertyMapping("block_hashes", "block_hashes")
    ]
).build()


def block_next_get() -> bytearray:
    return BlockFileJSONEncoder().default(_block_file_generator.create_random_file())
