"""Tests for ContentCache LRU caching implementation.

This module validates the ContentCache class including:
- LRU eviction logic
- Mtime-based invalidation
- Cache statistics tracking
- Concurrent access safety
"""

import pytest
import asyncio
from skillkit.core.models import ContentCache, CacheStats


# ==============================================================================
# T020: ContentCache Unit Tests (User Story 1)
# ==============================================================================


@pytest.mark.asyncio
async def test_cache_get_miss_returns_none():
    """Validate get() returns None for cache miss.

    Tests that attempting to retrieve non-existent cache entry
    returns None and increments miss counter.
    """
    cache = ContentCache(max_size=10)

    result = await cache.get("skill-name", "args", 1000.0)

    assert result is None

    stats = cache.get_stats()
    assert stats.misses == 1
    assert stats.hits == 0


@pytest.mark.asyncio
async def test_cache_put_and_get_success():
    """Validate put() stores and get() retrieves content.

    Tests basic cache storage and retrieval with valid mtime.
    """
    cache = ContentCache(max_size=10)

    await cache.put("skill-name", "args", "content", 1000.0)
    result = await cache.get("skill-name", "args", 1000.0)

    assert result == "content"

    stats = cache.get_stats()
    assert stats.hits == 1
    assert stats.misses == 0
    assert stats.size == 1


@pytest.mark.asyncio
async def test_cache_lru_eviction_at_capacity():
    """Validate LRU eviction when cache reaches max_size.

    Tests that oldest entry is evicted when cache is full
    and new entry is added.
    """
    cache = ContentCache(max_size=3)

    # Fill cache to capacity
    await cache.put("skill1", "args", "content1", 1000.0)
    await cache.put("skill2", "args", "content2", 1000.0)
    await cache.put("skill3", "args", "content3", 1000.0)

    # Verify all 3 entries present
    stats = cache.get_stats()
    assert stats.size == 3

    # Add 4th entry - should evict skill1 (oldest)
    await cache.put("skill4", "args", "content4", 1000.0)

    # Verify skill1 evicted, skill4 present
    result1 = await cache.get("skill1", "args", 1000.0)
    assert result1 is None  # Evicted

    result4 = await cache.get("skill4", "args", 1000.0)
    assert result4 == "content4"  # Present

    stats = cache.get_stats()
    assert stats.size == 3  # Still at capacity


@pytest.mark.asyncio
async def test_cache_lru_move_to_end_on_access():
    """Validate LRU move-to-end on cache hit.

    Tests that accessing a cache entry marks it as recently used
    and prevents it from being evicted.
    """
    cache = ContentCache(max_size=3)

    # Fill cache
    await cache.put("skill1", "args", "content1", 1000.0)
    await cache.put("skill2", "args", "content2", 1000.0)
    await cache.put("skill3", "args", "content3", 1000.0)

    # Access skill1 (mark as recently used)
    result = await cache.get("skill1", "args", 1000.0)
    assert result == "content1"

    # Add skill4 - should evict skill2 (now oldest)
    await cache.put("skill4", "args", "content4", 1000.0)

    # Verify skill1 still present (was marked recent)
    result1 = await cache.get("skill1", "args", 1000.0)
    assert result1 == "content1"

    # Verify skill2 evicted
    result2 = await cache.get("skill2", "args", 1000.0)
    assert result2 is None


@pytest.mark.asyncio
async def test_cache_mtime_invalidation():
    """Validate cache invalidation when file mtime increases.

    Tests that stale cache entries (mtime < file_mtime) are
    automatically invalidated and removed.
    """
    cache = ContentCache(max_size=10)

    # Cache content with mtime 1000.0
    await cache.put("skill", "args", "old_content", 1000.0)

    # Retrieve with same mtime - cache hit
    result1 = await cache.get("skill", "args", 1000.0)
    assert result1 == "old_content"
    assert cache.get_stats().hits == 1

    # File modified (mtime increased to 2000.0)
    result2 = await cache.get("skill", "args", 2000.0)
    assert result2 is None  # Invalidated
    assert cache.get_stats().misses == 1

    # Cache should be empty now (invalidated entry removed)
    stats = cache.get_stats()
    assert stats.size == 0


@pytest.mark.asyncio
async def test_cache_mtime_exact_match_valid():
    """Validate cache hit when mtimes match exactly.

    Tests that cached_mtime == file_mtime is considered valid.
    """
    cache = ContentCache(max_size=10)

    await cache.put("skill", "args", "content", 1500.5)

    # Exact mtime match - cache valid
    result = await cache.get("skill", "args", 1500.5)
    assert result == "content"
    assert cache.get_stats().hits == 1


@pytest.mark.asyncio
async def test_cache_mtime_newer_cached_valid():
    """Validate cache hit when cached_mtime >= file_mtime.

    Tests that cached content is valid if cached_mtime is newer
    than or equal to current file_mtime.
    """
    cache = ContentCache(max_size=10)

    # Cache with mtime 2000.0
    await cache.put("skill", "args", "content", 2000.0)

    # File mtime 1500.0 (older than cached) - cache valid
    result = await cache.get("skill", "args", 1500.0)
    assert result == "content"
    assert cache.get_stats().hits == 1


@pytest.mark.asyncio
async def test_cache_statistics_tracking():
    """Validate cache statistics (hits, misses, size, hit_rate).

    Tests that CacheStats accurately tracks cache operations
    and calculates hit rate.
    """
    cache = ContentCache(max_size=10)

    # Initial stats
    stats = cache.get_stats()
    assert stats.size == 0
    assert stats.max_size == 10
    assert stats.hits == 0
    assert stats.misses == 0
    assert stats.hit_rate == 0.0

    # Miss
    await cache.get("skill", "args", 1000.0)
    stats = cache.get_stats()
    assert stats.misses == 1
    assert stats.hit_rate == 0.0  # 0 / 1

    # Put and hit
    await cache.put("skill", "args", "content", 1000.0)
    await cache.get("skill", "args", 1000.0)
    stats = cache.get_stats()
    assert stats.hits == 1
    assert stats.misses == 1
    assert stats.size == 1
    assert stats.hit_rate == 0.5  # 1 / 2

    # Multiple hits
    for _ in range(4):
        await cache.get("skill", "args", 1000.0)

    stats = cache.get_stats()
    assert stats.hits == 5
    assert stats.misses == 1
    assert stats.hit_rate == 5 / 6  # 5 / (5 + 1)


@pytest.mark.asyncio
async def test_cache_clear_all():
    """Validate clear() removes all cache entries.

    Tests that calling clear() without skill_name removes
    all cached content and resets size.
    """
    cache = ContentCache(max_size=10)

    # Add multiple entries
    await cache.put("skill1", "args", "content1", 1000.0)
    await cache.put("skill2", "args", "content2", 1000.0)
    await cache.put("skill3", "args", "content3", 1000.0)

    stats = cache.get_stats()
    assert stats.size == 3

    # Clear all
    cleared = await cache.clear()
    assert cleared == 3

    # Verify cache empty
    stats = cache.get_stats()
    assert stats.size == 0

    # Verify entries removed
    result = await cache.get("skill1", "args", 1000.0)
    assert result is None


@pytest.mark.asyncio
async def test_cache_clear_specific_skill():
    """Validate clear(skill_name) removes only that skill's entries.

    Tests that calling clear() with specific skill_name removes
    only entries for that skill, preserving others.
    """
    cache = ContentCache(max_size=10)

    # Add entries for multiple skills
    await cache.put("skill1", "args1", "content1", 1000.0)
    await cache.put("skill1", "args2", "content2", 1000.0)
    await cache.put("skill2", "args1", "content3", 1000.0)

    stats = cache.get_stats()
    assert stats.size == 3

    # Clear only skill1
    cleared = await cache.clear(skill_name="skill1")
    assert cleared == 2  # Two entries for skill1

    # Verify skill1 entries removed
    result1 = await cache.get("skill1", "args1", 1000.0)
    assert result1 is None

    result2 = await cache.get("skill1", "args2", 1000.0)
    assert result2 is None

    # Verify skill2 entry still present
    result3 = await cache.get("skill2", "args1", 1000.0)
    assert result3 == "content3"

    stats = cache.get_stats()
    assert stats.size == 1


@pytest.mark.asyncio
async def test_cache_different_arguments_separate_entries():
    """Validate different arguments create separate cache entries.

    Tests that (skill_name, args1) and (skill_name, args2) are
    treated as distinct cache keys.
    """
    cache = ContentCache(max_size=10)

    await cache.put("skill", "args1", "content1", 1000.0)
    await cache.put("skill", "args2", "content2", 1000.0)

    result1 = await cache.get("skill", "args1", 1000.0)
    result2 = await cache.get("skill", "args2", 1000.0)

    assert result1 == "content1"
    assert result2 == "content2"

    stats = cache.get_stats()
    assert stats.size == 2  # Two separate entries


@pytest.mark.asyncio
async def test_cache_update_existing_entry():
    """Validate put() updates existing cache entry.

    Tests that calling put() with same key updates content
    and mtime without creating duplicate entry.
    """
    cache = ContentCache(max_size=10)

    # Initial put
    await cache.put("skill", "args", "old_content", 1000.0)
    stats = cache.get_stats()
    assert stats.size == 1

    # Update same key
    await cache.put("skill", "args", "new_content", 2000.0)
    stats = cache.get_stats()
    assert stats.size == 1  # Still only 1 entry

    # Verify updated content
    result = await cache.get("skill", "args", 2000.0)
    assert result == "new_content"


@pytest.mark.asyncio
async def test_cache_concurrent_access_different_skills():
    """Validate concurrent access to different skills is safe.

    Tests that multiple concurrent operations on different
    cache keys complete successfully without race conditions.
    """
    cache = ContentCache(max_size=100)

    async def put_and_get(skill_name: str, args: str):
        await cache.put(skill_name, args, f"content-{skill_name}", 1000.0)
        result = await cache.get(skill_name, args, 1000.0)
        assert result == f"content-{skill_name}"

    # Launch 10 concurrent tasks
    tasks = [
        put_and_get(f"skill-{i}", "args")
        for i in range(10)
    ]
    await asyncio.gather(*tasks)

    # Verify all entries cached
    stats = cache.get_stats()
    assert stats.size == 10
    assert stats.hits == 10  # All gets succeeded


@pytest.mark.asyncio
async def test_cache_empty_after_initialization():
    """Validate cache starts empty with zero statistics.

    Tests initial state of cache after construction.
    """
    cache = ContentCache(max_size=50)

    stats = cache.get_stats()

    assert stats.size == 0
    assert stats.max_size == 50
    assert stats.hits == 0
    assert stats.misses == 0
    assert stats.hit_rate == 0.0
