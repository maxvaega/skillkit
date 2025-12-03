# Core Features

This document provides detailed information about skillkit's core features and advanced usage patterns.

## Table of Contents

- [Script Execution](#script-execution)
- [Caching System](#caching-system)
- [Multi-Source Discovery](#multi-source-discovery)
- [Common Usage Patterns](#common-usage-patterns)
- [Debugging Tips](#debugging-tips)
- [Performance Tips](#performance-tips)

---

## Script Execution

Skills can include executable scripts for deterministic operations, combining AI reasoning with code execution. Scripts are automatically detected and can be executed with security controls.

### Supported Script Types

- **Python** (`.py`) - Python 3.x scripts
- **Shell** (`.sh`) - Bash shell scripts
- **JavaScript** (`.js`) - Node.js scripts
- **Ruby** (`.rb`) - Ruby scripts
- **Perl** (`.pl`) - Perl scripts
- **Windows** (`.bat`, `.cmd`, `.ps1`) - Batch and PowerShell scripts

### Basic Script Execution

```python
from skillkit import SkillManager

manager = SkillManager()
manager.discover()

# Execute a script from a skill
result = manager.execute_skill_script(
    skill_name="pdf-extractor",
    script_name="extract",
    arguments={"file": "document.pdf", "pages": "all"},
    timeout=30  # optional, defaults to 30 seconds
)

if result.success:
    print(result.stdout)  # Script output
else:
    print(f"Error: {result.stderr}")
    print(f"Exit code: {result.exit_code}")
```

### Script Directory Structure

Scripts should be placed in a `scripts/` directory or in the skill root:

```
my-skill/
├── SKILL.md
└── scripts/
    ├── extract.py
    ├── convert.sh
    └── utils/
        └── parser.py
```

### Script Input/Output

Scripts receive arguments as JSON via stdin and should output results to stdout.

**Important**: All parameter names are **automatically normalized to lowercase** by the core `execute_skill_script` method. This ensures consistent handling across all framework integrations (LangChain, LlamaIndex, CrewAI, etc.), regardless of how LLMs or developers capitalize parameter names.

**Best Practice**: Always use lowercase parameter names in your scripts:

```python
#!/usr/bin/env python3
"""Extract data from PDF file."""
import sys
import json

# Read arguments from stdin
args = json.load(sys.stdin)

# ✅ Use lowercase parameter names for compatibility
file_path = args.get('file_path', 'document.pdf')
page_range = args.get('page_range', 'all')

# Process data
result = {"extracted_text": "..."}

# Output JSON to stdout
print(json.dumps(result))
```

**Example**: If an LLM generates `{'File_Path': 'doc.pdf', 'Page_Range': '1-5'}`, skillkit automatically converts it to `{'file_path': 'doc.pdf', 'page_range': '1-5'}` before passing to your script. This normalization happens in the core manager, benefiting all framework integrations.

### Environment Variables

Scripts automatically receive these environment variables:

- `SKILL_NAME` - Name of the parent skill
- `SKILL_BASE_DIR` - Absolute path to skill directory
- `SKILL_VERSION` - Skill version from metadata
- `SKILLKIT_VERSION` - Current skillkit version

```python
import os

skill_name = os.environ['SKILL_NAME']
skill_dir = os.environ['SKILL_BASE_DIR']
```

### Error Handling

```python
from skillkit.core.exceptions import (
    ScriptNotFoundError,
    InterpreterNotFoundError,
    PathSecurityError,
    ToolIDValidationError
)

try:
    result = manager.execute_skill_script(
        skill_name="my-skill",
        script_name="process",
        arguments={"data": [1, 2, 3]}
    )
except ScriptNotFoundError:
    print("Script not found in skill")
except InterpreterNotFoundError:
    print("Required interpreter not available")
except PathSecurityError:
    print("Security validation failed")
```

### Execution Result Properties

The `ScriptExecutionResult` object provides detailed execution information:

```python
result = manager.execute_skill_script(...)

result.exit_code          # Process exit code (0 = success)
result.success            # True if exit_code == 0
result.stdout             # Captured standard output
result.stderr             # Captured standard error
result.execution_time_ms  # Execution duration in milliseconds
result.timeout            # True if script was killed by timeout
result.signaled           # True if terminated by signal
result.signal             # Signal name (e.g., 'SIGSEGV')
result.stdout_truncated   # True if output exceeded 10MB
result.stderr_truncated   # True if stderr exceeded 10MB
```

### Examples

Complete working examples available in `examples/`:

- **examples/script_execution.py** - Basic execution, error handling, timeouts
- **examples/langchain_agent.py** - LangChain integration with script tools
- **examples/skills/pdf-extractor/** - Real-world skill with multiple scripts

---

## Caching System

### Performance Note ⚡

With v0.4's advanced caching, repeated skill invocations are **up to 25x faster**:
- **First invocation**: ~10-25ms (loads from disk)
- **Cached invocations**: <1ms (memory lookup)
- **Automatic**: No code changes needed, cache works transparently

### Cache Performance Monitoring

```python
from skillkit import SkillManager

# Create manager with custom cache size
manager = SkillManager(max_cache_size=200)  # Default: 100
manager.discover()

# First invocation - cache miss (~10-25ms)
result1 = manager.invoke_skill("code-reviewer", "Review main.py")

# Second invocation - cache hit (<1ms)
result2 = manager.invoke_skill("code-reviewer", "Review main.py")

# Monitor cache performance
stats = manager.get_cache_stats()
print(f"Cache hit rate: {stats.hit_rate:.1%}")
print(f"Cache usage: {stats.size}/{stats.max_size}")
print(f"Total hits: {stats.hits}, Total misses: {stats.misses}")

# Clear cache when needed
manager.clear_cache("code-reviewer")  # Clear specific skill
manager.clear_cache()  # Clear all cache entries
```

---

## Multi-Source Discovery

### Multi-Source Discovery with Priority Resolution

```python
from skillkit import SkillManager

# Configure multiple skill sources
manager = SkillManager(
    project_skill_dir="./skills",              # Priority: 100 (highest)
    anthropic_config_dir="./.claude/skills",  # Priority: 50
    plugin_dirs=[                              # Priority: 10 each
        "./plugins/data-tools",
        "./plugins/web-tools"
    ],
    additional_search_paths=["./shared"]      # Priority: 5
)

manager.discover()

# Simple name gets highest priority version
skill = manager.get_skill("csv-parser")  # Gets project version if exists

# Qualified name accesses specific plugin version
skill = manager.get_skill("data-tools:csv-parser")  # Explicit plugin version
```

---

## Common Usage Patterns

### Custom skills directory

```python
from pathlib import Path

manager = SkillManager(project_skill_dir=Path("/custom/skills"))
```

### Error handling

```python
from skillkit import SkillNotFoundError, ContentLoadError

try:
    result = manager.invoke_skill("my-skill", args)
except SkillNotFoundError:
    print("Skill not found")
except ContentLoadError:
    print("Skill file was deleted or is unreadable")
```

### Accessing metadata

```python
metadata = manager.get_skill("code-reviewer")
print(f"Path: {metadata.skill_path}")
print(f"Tools: {metadata.allowed_tools}")
```

### Multiple arguments

```python
# Arguments are passed as a single string
result = manager.invoke_skill("code-reviewer", "Review file.py for security issues")
```

### No placeholder behavior

If SKILL.md has no `$ARGUMENTS` placeholder:
- With arguments: appended to end of content
- Without arguments: content returned unchanged

---

## Debugging Tips

### Enable logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Module-specific logging

```python
logging.getLogger('skillkit.core.discovery').setLevel(logging.DEBUG)
```

### Common issues

**Skill not found after discovery:**
- Check skill directory path
- Verify SKILL.md file exists (case-insensitive)
- Check logs for parsing errors

**YAML parsing errors:**
- Validate YAML syntax (use yamllint)
- Check for proper `---` delimiters
- Ensure required fields present

**Arguments not substituted:**
- Check for `$ARGUMENTS` placeholder (case-sensitive)
- Check for typos: `$arguments`, `$ARGUMENT`, `$ ARGUMENTS`
- See logs for typo detection warnings

**Memory usage concerns:**
- Content is loaded lazily (only when `.content` accessed or `invoke()` called)
- Python 3.10+ recommended for optimal memory efficiency (60% reduction via slots)

---

## Performance Tips

1. **Discover once**: Call `discover()` once at startup, reuse manager
2. **Reuse manager**: Don't create new SkillManager for each invocation - cache is instance-level
3. **Monitor cache**: Use `get_cache_stats()` to verify good hit rates (target: >80%)
4. **Configure cache size**: Increase `max_cache_size` for agents with many skills or diverse arguments
5. **Keep skills focused**: Large skills (>200KB) may slow down invocation
6. **Use Python 3.10+**: Better memory efficiency with dataclass slots
7. **Use async methods**: `ainvoke_skill()` enables concurrent skill execution
