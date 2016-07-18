from cacheanalysis.models import BlockFile, CacheMissRecord, CacheHitRecord
from hgijson import MappingJSONEncoderClassBuilder, JsonPropertyMapping

from cacheusagesimulator.file_generator import BlockFileGenerator
from cacheusagesimulator.usage_generator import UsageGenerator

_block_file_generator = BlockFileGenerator(blocks_per_file_spread=0)
_usage_generator = UsageGenerator().generate()


BlockFileJSONEncoder = MappingJSONEncoderClassBuilder(
    BlockFile,
    [
        JsonPropertyMapping("name", "name"),
        JsonPropertyMapping("block_hashes", "block_hashes")
    ]
).build()


def get_random_block_file() -> dict:
    return BlockFileJSONEncoder().default(_block_file_generator.create_random_file())


def get_next_block() -> dict:
    while True:
        record = next(_usage_generator)
        if isinstance(record, CacheHitRecord) or isinstance(record, CacheMissRecord):
            return {"hash": record.block_hash}