from typing import Dict, List, Iterable, Set

from hgijson import MappingJSONEncoderClassBuilder, JsonPropertyMapping

from cacheanalysis.models import BlockFile, CacheMissRecord, CacheHitRecord
from cacheusagesimulator.file_generator import BlockFileGenerator
from cacheusagesimulator.usage_generator import UsageGenerator

_block_file_generator = BlockFileGenerator(blocks_per_file_spread=0)
_usage_generator = UsageGenerator()
_cache_misses = dict()    # type: Dict[str, CacheMissRecord]


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
        record = _usage_generator.generate()
        if isinstance(record, CacheMissRecord):
            if record.block_hash not in _cache_misses:
                _cache_misses[record.block_hash] = record

        if isinstance(record, CacheHitRecord) or isinstance(record, CacheMissRecord):
            return record.block_hash


def get_reference_blocks() -> List[dict]:
    return list(_get_block_hashes_from_files(_usage_generator.known_reference_files))


def get_non_reference_blocks() -> List[dict]:
    return list(_get_block_hashes_from_files(_usage_generator.known_non_reference_files))


def _get_block_hashes_from_files(files: Iterable[BlockFile]) -> Set[str]:
    blocks = set()
    for blockfile in files:
        for block_hash in blockfile.block_hashes:
            blocks.add(block_hash)
    return list(blocks)
