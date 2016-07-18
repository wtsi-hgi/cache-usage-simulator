from typing import List

from cacheanalysis.json_converters import BlockFileJSONEncoder
from cacheanalysis.models import CacheMissRecord, CacheHitRecord
from cacheusagesimulator.file_generator import BlockFileGenerator
from cacheusagesimulator.usage_generator import UsageGenerator

_block_file_generator = BlockFileGenerator(blocks_per_file_spread=0)
_usage_generator = UsageGenerator()


def get_random_block_file() -> dict:
    return BlockFileJSONEncoder().default(_block_file_generator.create_random_file())


def get_next_block() -> dict:
    while True:
        record = _usage_generator.generate()
        if isinstance(record, CacheHitRecord) or isinstance(record, CacheMissRecord):
            return record.block_hash


def get_reference_files() -> List[dict]:
    return BlockFileJSONEncoder().default(_usage_generator.known_reference_files)


def get_non_reference_files() -> List[dict]:
    return BlockFileJSONEncoder().default(_usage_generator.known_non_reference_files)
