<div align="center">
<h1 align="center" style="font-size:4em">skillkit</h1>
</div>
<p align="center" style="max-width:80%; margin-bottom:40px">Enables Anthropic's Agent Skills functionality to any python agent, unleashing LLM-powered agents to <b>autonomously discover and utilize packaged expertise</b> in a token-efficient way.
skillkit is compatible with existings skills (SKILL.md), so you can browse and use any skill available on the web</p>

<p align="center">
<a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.10%2B-blue" /></a>
<a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" /></a>
<a href="https://pypi.org/project/skillkit/">
    <img src="https://img.shields.io/pypi/v/skillkit" /></a>
<a href="ttps://github.com/maxvaega/skillkit/releases">
    <img src="https://img.shields.io/github/v/release/maxvaega/skillkit" /></a>
<a href="https://github.com/maxvaega/skillkit/stargazers">
    <img src="https://img.shields.io/github/stars/maxvaega/skillkit" /></a>
</p>

<div align="center">
<img src="https://i.imgflip.com/addac0.jpg" title="skillkit for developers" width=370px height=250px/>
</div>

---

## Features

- **Framework-free**: can be used without any framework, or with other frameworks (currently only compatible with LangChain - more coming in the future!)
- **Fully compatible with existing skills**: existing skills can be copied directly, no change needed
- **Model-agnostic**: Works with any LLM
- **Multi-source skill discovery**: From project, Anthropic config, plugins, and custom directories with priority-based conflict resolution
- **YAML frontmatter parsing** with comprehensive validation
- **Progressive disclosure pattern** (metadata-first loading, 80% memory reduction, Level 2 content caching)
- **Script execution**: Execute Python, Shell, JavaScript, Ruby, and Perl scripts from skills with comprehensive security controls
- **Plugin ecosystem**: Full support for Anthropic's MCPB plugin manifests with namespaced skill access
- **Nested directory structures**: Discover skills in any directory hierarchy up to 5 levels deep
- **Security features**: Input validation, size limits, suspicious pattern detection, path security, secure file resolution, script sandboxing

---

## Why Skills Matter?

### What Skills Are

**Agent Skills** are modular capability packages that work like "onboarding guides" for AI. Each skill is a folder containing a **SKILL.md** file (with YAML metadata + Markdown instructions) plus optional supporting files like scripts, templates, and documentation. The Agent autonomously discovers and loads skills based on task relevance using a progressive disclosure model—first reading just the name/description metadata, then the full SKILL.md if needed, and finally any referenced files only when required.

### Why Skills Matter

**-  Transform AI from assistant to operational team member** — Skills let you encode your organization's procedural knowledge, workflows, and domain expertise into reusable capabilities that Claude can invoke autonomously. Instead of repeatedly prompting Claude with the same context, you create persistent "muscle memory" that integrates AI into real business processes, making it a specialized professional rather than a generic chatbot.

**-  Combine AI reasoning with deterministic code execution** — Skills can bundle Python, Shell, JavaScript, Ruby, and Perl scripts alongside natural language instructions, letting AI use traditional programming for tasks where LLMs are wasteful or unreliable (like sorting lists, filling PDF forms, or data transformations). This hybrid approach delivers the reliability of code with the flexibility of AI reasoning, ensuring consistent, auditable results for mission-critical operations. 

**-  Achieve scalable efficiency through progressive disclosure** — Unlike traditional prompting where everything loads into context, skills use a three-tier discovery system (metadata → full instructions → supplementary files) that **keeps Claude's context window lean**. This architecture allows unlimited expertise to be available without token bloat, dramatically **reducing running costs** while supporting dozens of skills simultaneously.

### Where can i find ready-to-use skills?

The web is full of great skills! here are some repositories you can check out:
- [Anthropic Skills Library](https://github.com/anthropics/skills)
- [Claude-Plugins.dev Library](https://claude-plugins.dev/skills)
- [travisvn/awesome-claude-skills repo](https://github.com/travisvn/awesome-claude-skills)
- [maxvaega/awesome-skills repo](https://github.com/maxvaega/awesome-skills)

---

## Installation

### Core library (includes async support)

```bash
pip install skillkit
```

### With LangChain integration

```bash
pip install skillkit[langchain]
```

### All extras (LangChain + dev tools)

```bash
pip install skillkit[all]
```

### Development dependencies

```bash
pip install skillkit[dev]
```

## Quick Start

### Performance Note ⚡

With v0.4's advanced caching, repeated skill invocations are **up to 25x faster**:
- **First invocation**: ~10-25ms (loads from disk)
- **Cached invocations**: <1ms (memory lookup)
- **Automatic**: No code changes needed, cache works transparently

### 1. Create a skill

Create a directory structure:
```
.claude/skills/code-reviewer/SKILL.md
```

SKILL.md format:
```markdown
---
name: code-reviewer
description: Review code for best practices and potential issues
allowed-tools: Read, Grep
---

# Code Reviewer Skill

You are a code reviewer. Analyze the provided code for:
- Best practices violations
- Potential bugs
- Security vulnerabilities

## Instructions

$ARGUMENTS
```

### 2. Use standalone (without frameworks)

#### Simple usage

```python
from skillkit import SkillManager

# Create manager (defaults to ./.claude/skills/)
manager = SkillManager()

# Discover skills
manager.discover()

# List available skills
for skill in manager.list_skills():
    print(f"{skill.name}: {skill.description}")

# Invoke a skill
result = manager.invoke_skill("code-reviewer", "Review function calculate_total()")
print(result)
```

### 3. Use with LangChain

```python
from skillkit import SkillManager
from skillkit.integrations.langchain import create_langchain_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage

# Discover skills
manager = SkillManager()
manager.discover()

# Convert to LangChain tools
tools = create_langchain_tools(manager)

# Create agent
llm = ChatOpenAI(model="gpt-5.1")
prompt = "You are a helpful assistant. use the available skills tools to answer the user queries."
agent = create_agent(
    llm, 
    tools, 
    system_prompt=prompt
    )

# Use agent
query="What are Common Architectural Scenarios in python?"
messages = [HumanMessage(content=query)]
result = agent.invoke({"messages": messages})
```

### Async LangChain Integration

```python
import asyncio
from skillkit import SkillManager
from skillkit.integrations.langchain import create_langchain_tools
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI

async def run_agent():
    manager = SkillManager()
    await manager.adiscover()

    tools = create_langchain_tools(manager)
    prompt = "You are a helpful assistant. use the available skills tools to answer the user queries."
    llm = ChatOpenAI(model="gpt-5.1")

    agent = create_agent(
        llm,
        tools,
        system_prompt=prompt
        )

    query="What are Common Architectural Scenarios in python?"
    messages = [HumanMessage(content=query)]
    result = await agent.ainvoke({"messages": messages})

asyncio.run(run_agent())
```

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

### Cache Performance Monitoring (requires v0.4+)

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

## SKILL.md Format

### Required Fields

- `name` (string): Unique skill identifier
- `description` (string): Human-readable skill description

### Optional Fields

- `allowed-tools` (list): Tool names allowed for this skill (not enforced in v0.1)

### Example

```yaml
---
name: git-helper
description: Generate git commit messages and workflow guidance
allowed-tools: Bash, Read
---

# Git Helper Skill

Content with $ARGUMENTS placeholder...
```

### Argument Substitution

- `$ARGUMENTS` → replaced with user-provided arguments
- `$$ARGUMENTS` → literal `$ARGUMENTS` (escaped)
- No placeholder + arguments → arguments appended to end
- No placeholder + no arguments → content unchanged

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

### LangChain Integration

Scripts are automatically exposed as separate LangChain tools:

```python
from skillkit import SkillManager
from skillkit.integrations.langchain import create_langchain_tools

manager = SkillManager()
manager.discover()

# Each script becomes a separate tool: "{skill-name}__{script-name}"
tools = create_langchain_tools(manager)

# Example tool names:
# - "pdf-extractor__extract"
# - "pdf-extractor__convert"
# - "pdf-extractor__parse"
```

#### Tool ID Format and Validation

Script tool IDs follow a validated format to ensure LLM provider compatibility:

- **Format**: `{skill-name}__{script-name}` (double underscore separator)
- **Validation Pattern**: `^[a-z0-9-]+__[a-z0-9_]+$`
- **Max Length**: 60 characters
- **Automatic Normalization**:
  - Skill names: Lowercase with underscores converted to hyphens
  - Script names: Lowercase with underscores preserved

```python
# Examples of valid tool IDs:
# ✓ "pdf-extractor__extract" (skill: PDF-Extractor, script: extract.py)
# ✓ "csv-parser__parse" (skill: csv_parser, script: parse.py)
# ✓ "data-processor__transform-json" (skill: DataProcessor, script: transform_json.py)

# Invalid formats raise ToolIDValidationError:
# ✗ "pdf.extractor__extract" (dots not allowed in skill name)
# ✗ "PDF-Extractor__Extract" (uppercase not allowed)
# ✗ "very-long-skill-name-exceeds-limit__script" (exceeds 60 chars)
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

## Performance Tips

1. **Discover once**: Call `discover()` once at startup, reuse manager
2. **Reuse manager**: Don't create new SkillManager for each invocation - cache is instance-level
3. **Monitor cache**: Use `get_cache_stats()` to verify good hit rates (target: >80%)
4. **Configure cache size**: Increase `max_cache_size` for agents with many skills or diverse arguments
5. **Keep skills focused**: Large skills (>200KB) may slow down invocation
6. **Use Python 3.10+**: Better memory efficiency with dataclass slots
7. **Use async methods**: `ainvoke_skill()` enables concurrent skill execution

## Requirements

- **Python**: 3.10+
- **Core dependencies**: PyYAML 6.0+
- **Optional**: langchain-core 0.1.0+, pydantic 2.0+ (for LangChain integration)

## Development

### Setup

```bash
git clone https://github.com/maxvaega/skillkit.git
cd skillkit
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Run tests

The project includes a comprehensive pytest-based test suite with 70%+ coverage validating core functionality, integrations, and edge cases.
For detailed testing instructions, test organization, markers, and debugging tips, see **[tests/README.md](tests/README.md)**.

## Examples

See `examples/` directory:
- `basic_usage.py` - Standalone usage (sync and async patterns)
- `async_usage.py` - Async usage with FastAPI integration
- `langchain_agent.py` - LangChain agent integration (sync and async)
- `multi_source.py` - Multi-source discovery and conflict resolution
- `file_references.py` - Secure file path resolution
- `caching_demo.py` ⚡ NEW - Cache performance demonstration
- `skills/` - Example skills and plugins

Run examples:
```bash
# Basic sync usage
python examples/basic_usage.py

# Async usage with FastAPI
python examples/async_usage.py

# LangChain integration
python examples/langchain_agent.py

# Multi-source discovery
python examples/multi_source.py

# File path resolution
python examples/file_references.py

# Cache performance demo (NEW in v0.4)
python examples/caching_demo.py
```

## Roadmap

### v0.1 (Released)
- ✅ Core skill discovery and metadata management
- ✅ YAML frontmatter parsing with validation
- ✅ Progressive disclosure pattern (lazy loading)
- ✅ Skill invocation with argument substitution
- ✅ LangChain integration (sync only)
- ✅ 70% test coverage

### v0.2 (Released) ✨
- ✅ Async support (`adiscover()`, `ainvoke_skill()`)
- ✅ Multi-source discovery (project, Anthropic config, plugins, custom paths)
- ✅ Plugin integration with MCPB manifest support
- ✅ Nested directory structures (up to 5 levels deep)
- ✅ Fully qualified skill names for conflict resolution
- ✅ Secure file path resolution with traversal prevention
- ✅ LangChain async integration (`ainvoke`)
- ✅ Backward compatible with v0.1

### v0.3 (Released) 🚀
- ✅ Script Execution Support (Python, Shell, JavaScript, Ruby, Perl)
- ✅ Automatic script detection (recursive, up to 5 levels)
- ✅ Security controls (path validation, permission checks, timeout enforcement)
- ✅ Environment variable injection (SKILL_NAME, SKILL_BASE_DIR, SKILL_VERSION, SKILLKIT_VERSION)
- ✅ LangChain script tool integration (each script exposed as separate StructuredTool)
- ✅ Parameters normalization to lower-case
- ✅ Comprehensive error handling and audit logging
- ✅ Cross-platform support (Linux, macOS, Windows)
- ✅ Backward compatible with v0.1/v0.2 (except ToolRestrictionError removed)

### v0.4 (Released) ⚡
- ✅ Advanced Progressive Disclosure with LRU content caching
- ✅ Mtime-based automatic cache invalidation
- ✅ Argument normalization for maximum cache efficiency
- ✅ Thread-safe concurrent invocations with per-skill asyncio locks
- ✅ Cache management API (get_cache_stats(), clear_cache())
- ✅ Performance: <1ms cache hits vs 10-25ms first invocation
- ✅ Memory efficient: ~2.1KB per cached entry
- ✅ 80%+ cache hit rate achievable
- ✅ Backward compatible with v0.1/v0.2/v0.3

### v0.5 (Planned)
- Additional framework integrations (LlamaIndex, CrewAI, Haystack)

### v0.6 (Planned)
- Scripts permissions enforcement
- Enhanced error handling and recovery
- Performance optimizations
- Skill name enforcement and controls

### v0.7 (Planned)
- Advanced file system support
- bedrock code interpreter support

### v1.0 (Planned)
- Comprehensive documentation
- 90% test coverage
- Production-ready stability
- Full plugin ecosystem support

## License

MIT License - see LICENSE file for details.

## Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, improving documentation, or creating new example skills, your help is appreciated.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Ensure all tests pass (`pytest`)
5. Ensure code quality checks pass (`ruff check`, `mypy --strict`)
6. Submit a pull request

### Detailed Guidelines

For comprehensive contribution guidelines, including:
- Development environment setup
- Code style and testing requirements
- PR submission process
- Bug reporting and feature requests

Please see **[CONTRIBUTING.md](CONTRIBUTING.md)** for detailed information.

## Support

- **Issues**: https://github.com/maxvaega/skillkit/issues
- **Documentation**: https://github.com/maxvaega/skillkit#readme

## Acknowledgments

- Inspired by Anthropic's Agent Skills functionality
- Built with Python, PyYAML, LangChain, Pydantic and Claude itself!
