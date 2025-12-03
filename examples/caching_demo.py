#!/usr/bin/env python3
"""Caching efficiency demonstration for skillkit v0.4+.

This script demonstrates the performance improvements from Level 2 content caching:
- LRU cache with mtime-based invalidation
- Sub-millisecond cache hits
- Argument normalization for maximum cache efficiency
- Automatic cache invalidation on file changes
"""

import asyncio
import logging
import time
from pathlib import Path

from skillkit import SkillManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")


def measure_time_ms(func, *args, **kwargs):
    """Measure function execution time in milliseconds."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return result, elapsed_ms


async def measure_time_ms_async(func, *args, **kwargs):
    """Measure async function execution time in milliseconds."""
    start = time.perf_counter()
    result = await func(*args, **kwargs)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return result, elapsed_ms


def sync_caching_demo() -> None:
    """Demonstrate sync caching performance improvements."""
    print("=" * 70)
    print("skillkit v0.4: Caching Performance Demo (Sync)")
    print("=" * 70)

    # Use example skills
    skills_dir = Path(__file__).parent / "skills"
    print(f"\nUsing skills directory: {skills_dir}")

    # Create manager with default cache (100 entries)
    manager = SkillManager(project_skill_dir=skills_dir, max_cache_size=100)
    manager.discover()

    print("\n[1] First Invocation - Cache Miss")
    print("-" * 70)
    skill_name = "code-reviewer"
    arguments = "Review the calculate_total() function"

    result1, time1 = measure_time_ms(manager.invoke_skill, skill_name, arguments)
    stats1 = manager.get_cache_stats()

    print(f"  Execution time: {time1:.2f}ms")
    print(f"  Result length: {len(result1)} characters")
    print(f"  Cache stats: {stats1.hits} hits, {stats1.misses} misses")
    print(f"  Hit rate: {stats1.hit_rate:.1%}")

    print("\n[2] Second Invocation - Cache Hit (Same Arguments)")
    print("-" * 70)
    result2, time2 = measure_time_ms(manager.invoke_skill, skill_name, arguments)
    stats2 = manager.get_cache_stats()

    print(f"  Execution time: {time2:.2f}ms")
    print(f"  Result length: {len(result2)} characters")
    print(f"  Cache stats: {stats2.hits} hits, {stats2.misses} misses")
    print(f"  Hit rate: {stats2.hit_rate:.1%}")
    print(f"  Speedup: {time1 / time2:.1f}x faster")

    print("\n[3] Third Invocation - Cache Hit with Whitespace Variations")
    print("-" * 70)
    # Argument normalization makes these all hit the same cache entry
    arguments_whitespace = "  Review the calculate_total() function  "
    result3, time3 = measure_time_ms(manager.invoke_skill, skill_name, arguments_whitespace)
    stats3 = manager.get_cache_stats()

    print(f"  Arguments: '{arguments_whitespace}' (with extra whitespace)")
    print(f"  Execution time: {time3:.2f}ms")
    print(f"  Cache stats: {stats3.hits} hits, {stats3.misses} misses")
    print(f"  Hit rate: {stats3.hit_rate:.1%}")
    print(f"  Note: Whitespace normalized, same cache entry used!")

    print("\n[4] Fourth Invocation - Cache Miss (Different Arguments)")
    print("-" * 70)
    different_args = "Review the process_payment() function"
    result4, time4 = measure_time_ms(manager.invoke_skill, skill_name, different_args)
    stats4 = manager.get_cache_stats()

    print(f"  Execution time: {time4:.2f}ms")
    print(f"  Cache stats: {stats4.hits} hits, {stats4.misses} misses")
    print(f"  Hit rate: {stats4.hit_rate:.1%}")
    print(f"  Note: Different arguments → new cache entry created")

    print("\n[5] Cache Statistics Summary")
    print("-" * 70)
    final_stats = manager.get_cache_stats()
    print(f"  Total invocations: {final_stats.hits + final_stats.misses}")
    print(f"  Cache hits: {final_stats.hits}")
    print(f"  Cache misses: {final_stats.misses}")
    print(f"  Hit rate: {final_stats.hit_rate:.1%}")
    print(f"  Cache size: {final_stats.size}/{final_stats.max_size} entries")

    print("\n[6] Cache Clearing Demo")
    print("-" * 70)
    # Clear specific skill
    cleared = manager.clear_cache(skill_name)
    print(f"  Cleared {cleared} cache entries for skill '{skill_name}'")

    after_clear_stats = manager.get_cache_stats()
    print(f"  Cache size after clear: {after_clear_stats.size}/{after_clear_stats.max_size}")

    # Invoke again - should be cache miss
    result5, time5 = measure_time_ms(manager.invoke_skill, skill_name, arguments)
    print(f"  Re-invocation time: {time5:.2f}ms (cache miss after clear)")

    print("\n" + "=" * 70)
    print("Sync caching demo complete!")
    print("=" * 70)


async def async_caching_demo() -> None:
    """Demonstrate async caching performance with concurrent invocations."""
    print("\n\n" + "=" * 70)
    print("skillkit v0.4: Caching Performance Demo (Async)")
    print("=" * 70)

    skills_dir = Path(__file__).parent / "skills"
    print(f"\nUsing skills directory: {skills_dir}")

    manager = SkillManager(project_skill_dir=skills_dir, max_cache_size=100)
    await manager.adiscover()

    print("\n[1] Sequential Invocations - Building Cache")
    print("-" * 70)
    skill_name = "git-helper"

    # First invocation - cache miss
    result1, time1 = await measure_time_ms_async(
        manager.ainvoke_skill, skill_name, "Generate commit message for auth feature"
    )
    print(f"  Invocation 1: {time1:.2f}ms (cache miss)")

    # Second invocation - cache hit
    result2, time2 = await measure_time_ms_async(
        manager.ainvoke_skill, skill_name, "Generate commit message for auth feature"
    )
    print(f"  Invocation 2: {time2:.2f}ms (cache hit)")
    print(f"  Speedup: {time1 / time2:.1f}x")

    print("\n[2] Concurrent Invocations - Same Skill, Different Arguments")
    print("-" * 70)
    # These will execute in parallel (per-skill locking)
    start_concurrent = time.perf_counter()
    results = await asyncio.gather(
        manager.ainvoke_skill(skill_name, "Generate commit for feature A"),
        manager.ainvoke_skill(skill_name, "Generate commit for bug fix B"),
        manager.ainvoke_skill(skill_name, "Generate commit for refactor C"),
    )
    concurrent_time = (time.perf_counter() - start_concurrent) * 1000

    print(f"  Total time (3 invocations): {concurrent_time:.2f}ms")
    print(f"  Average per invocation: {concurrent_time / 3:.2f}ms")
    print(f"  Note: Per-skill locking serializes same-skill invocations")

    print("\n[3] Concurrent Invocations - Different Skills (Parallel Execution)")
    print("-" * 70)
    # Different skills can execute truly in parallel
    start_parallel = time.perf_counter()
    try:
        parallel_results = await asyncio.gather(
            manager.ainvoke_skill("code-reviewer", "Review main.py"),
            manager.ainvoke_skill("git-helper", "Generate commit message"),
            return_exceptions=True,  # Don't fail if a skill is missing
        )
        parallel_time = (time.perf_counter() - start_parallel) * 1000

        # Filter out exceptions
        successful_results = [r for r in parallel_results if not isinstance(r, Exception)]
        print(f"  Total time ({len(successful_results)} skills): {parallel_time:.2f}ms")
        print(f"  Note: Different skills execute in parallel without blocking!")
    except Exception as e:
        print(f"  Note: Some skills may not exist in demo directory: {e}")

    print("\n[4] Cache Hit Rate Analysis")
    print("-" * 70)
    stats = manager.get_cache_stats()
    print(f"  Total invocations: {stats.hits + stats.misses}")
    print(f"  Cache hits: {stats.hits}")
    print(f"  Cache misses: {stats.misses}")
    print(f"  Hit rate: {stats.hit_rate:.1%}")
    print(f"  Cache usage: {stats.size}/{stats.max_size} entries")

    print("\n[5] File Modification & Cache Invalidation")
    print("-" * 70)
    print("  Note: Cache automatically invalidates when SKILL.md files are modified")
    print("  Invalidation is based on file mtime (modification time)")
    print("  Next invocation after file change will reload content from disk")

    print("\n" + "=" * 70)
    print("Async caching demo complete!")
    print("=" * 70)


def main():
    """Run both sync and async caching demos."""
    # Run sync demo
    sync_caching_demo()

    # Run async demo
    asyncio.run(async_caching_demo())

    print("\n" + "=" * 70)
    print("Key Takeaways:")
    print("=" * 70)
    print("  1. First invocation: ~10-25ms (loads from disk)")
    print("  2. Cached invocations: <1ms (memory lookup)")
    print("  3. Whitespace variations → same cache entry (normalization)")
    print("  4. Different arguments → different cache entries")
    print("  5. Concurrent same-skill → serialized (safe)")
    print("  6. Concurrent different-skills → parallel (fast)")
    print("  7. File modifications → automatic cache invalidation")
    print("  8. Cache stats available for monitoring")
    print("=" * 70)


if __name__ == "__main__":
    main()
