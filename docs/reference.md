# Reference

This document provides reference information for skillkit including SKILL.md format specification, system requirements, and development guidelines.

## Table of Contents

- [SKILL.md Format](#skillmd-format)
- [System Requirements](#system-requirements)
- [Development](#development)

---

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

---

## System Requirements

### Python Version

- **Python**: 3.10+

### Core Dependencies

- **Core dependencies**: PyYAML 6.0+

### Optional Dependencies

- **Optional**: langchain-core 0.1.0+, pydantic 2.0+ (for LangChain integration)

### Installation

```bash
# Core library (includes async support)
pip install skillkit

# With LangChain integration
pip install skillkit[langchain]

# All extras (LangChain + dev tools)
pip install skillkit[all]

# Development dependencies
pip install skillkit[dev]
```

---

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
For detailed testing instructions, test organization, markers, and debugging tips, see **[tests/README.md](../tests/README.md)**.

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test markers
pytest -m async          # Async tests only
pytest -m integration    # Integration tests only
pytest -m unit          # Unit tests only

# Run specific test file
pytest tests/test_manager.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Lint code
ruff check src/skillkit

# Format code
ruff format src/skillkit

# Type check
mypy src/skillkit --strict
```

### Running Examples

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

---

## API Overview

### SkillManager

Main orchestration class for skill discovery and invocation.

**Key Methods**:
- `discover()` - Synchronous skill discovery
- `adiscover()` - Async skill discovery
- `invoke_skill(name, args)` - Invoke a skill
- `ainvoke_skill(name, args)` - Async skill invocation
- `get_skill(name)` - Get skill metadata
- `list_skills()` - List all discovered skills
- `execute_skill_script(skill_name, script_name, arguments, timeout)` - Execute a script
- `get_cache_stats()` - Get cache statistics
- `clear_cache(skill_name)` - Clear cache entries

### SkillMetadata

Dataclass containing skill metadata (Level 1 of progressive disclosure).

**Key Fields**:
- `name: str` - Skill identifier
- `description: str` - Human-readable description
- `skill_path: Path` - Path to skill directory
- `allowed_tools: List[str]` - Allowed tool names
- `source: str` - Source location (project, plugin, etc.)
- `priority: int` - Discovery priority

### Skill

Dataclass containing full skill content (Level 2 of progressive disclosure).

**Key Fields**:
- `metadata: SkillMetadata` - Skill metadata
- `content: str` - Full SKILL.md content
- `scripts: List[ScriptMetadata]` - Available scripts

### Exception Hierarchy

```python
SkillKitError                    # Base exception
├── DiscoveryError               # Skill discovery failures
├── ParsingError                 # YAML parsing failures
├── SkillNotFoundError           # Skill not found
├── ContentLoadError             # Content loading failures
├── ArgumentSubstitutionError    # Argument substitution failures
├── ScriptNotFoundError          # Script not found
├── InterpreterNotFoundError     # Interpreter not available
├── PathSecurityError            # Path security validation failures
└── ToolIDValidationError        # Tool ID format validation failures
```

---

## Additional Resources

- **Core Features**: See [docs/core-features.md](core-features.md)
- **LangChain Integration**: See [docs/integration/langchain.md](integration/langchain.md)
- **Contributing**: See [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Examples**: See [examples/](../examples/) directory
