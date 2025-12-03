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

- **Fully compatible with existing skills**: existing skills can be copied directly, no change needed
- **Framework-free**: can be used without any framework, or with other frameworks (currently only compatible with LangChain - more coming in the future!)
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

## Insert additional instructions here


```

> **Learn more**: See [SKILL.md Format](docs/reference.md#skillmd-format) for full specification.

### 2. Use standalone (without frameworks)

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

> **Advanced patterns**: Multi-source discovery, async usage, error handling - see [Core Features](docs/core-features.md).

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
query="What does a code reviewer do?"
messages = [HumanMessage(content=query)]
result = agent.invoke({"messages": messages})
```

> **Learn more**: Async integration, script tools, advanced patterns - see [LangChain Integration Guide](docs/integration/langchain.md).

## SKILL.md Format

Skills are defined in SKILL.md files with YAML frontmatter:

```yaml
---
name: git-helper
description: Generate git commit messages and workflow guidance
allowed-tools: Bash, Read
---

# Git Helper Skill

Content placeholder...
Supports $ARGUMENTS...
```

**Required fields**: `name`, `description`
**Optional fields**: `allowed-tools`, `version`
**Argument substitution**: Use `$ARGUMENTS` placeholder (or `$$ARGUMENTS` for literal)

> **Full specification**: See [SKILL.md Format Reference](docs/reference.md#skillmd-format) for detailed rules and examples.

## Script Execution

Skills can include executable scripts (Python, Shell, JavaScript, Ruby, Perl) for deterministic operations, combining AI reasoning with code execution.

### Basic Example

```python
from skillkit import SkillManager

manager = SkillManager()
manager.discover()

# Execute a script from a skill
result = manager.execute_skill_script(
    skill_name="pdf-extractor",
    script_name="extract",
    arguments={"file": "document.pdf", "pages": "all"},
    timeout=30
)

if result.success:
    print(result.stdout)
else:
    print(f"Error: {result.stderr}")
```

**Key Features**:
- Automatic script detection in skill directories
- JSON input/output via stdin/stdout
- Environment variables (SKILL_NAME, SKILL_BASE_DIR, etc.)
- Automatic LangChain tool integration
- Security controls (path validation, timeout enforcement)

> **Full guide**: See [Script Execution](docs/core-features.md#script-execution) for directory structure, parameter normalization, error handling, and examples.

## Common Issues

**Skill not found:**
- Check skill directory path
- Verify SKILL.md file exists
- Check logs for parsing errors

**YAML parsing errors:**
- Validate YAML syntax (use yamllint)
- Check for proper `---` delimiters
- Ensure required fields present

**Arguments not substituted:**
- Check for `$ARGUMENTS` placeholder (case-sensitive)
- Check for typos: `$arguments`, `$ARGUMENT`

> **More help**: See [Debugging Tips](docs/core-features.md#debugging-tips) and [Performance Tips](docs/core-features.md#performance-tips) for detailed troubleshooting.

## Examples

See `examples/` directory:
- `basic_usage.py` - Standalone usage (sync and async patterns)
- `async_usage.py` - Async usage with FastAPI integration
- `langchain_agent.py` - LangChain agent integration (sync and async)
- `multi_source.py` - Multi-source discovery and conflict resolution
- `file_references.py` - Secure file path resolution
- `skills/` - Example skills and plugins
- `caching_demo.py` - Cache performance demonstration

## Roadmap

### v0.1 (Released)
- ✅ Core skill discovery and metadata management
- ✅ YAML frontmatter parsing with validation
- ✅ Progressive disclosure pattern (lazy loading)
- ✅ Skill invocation with argument substitution
- ✅ LangChain integration (sync only)
- ✅ 70% test coverage

### v0.2 (Released)
- ✅ Async support (`adiscover()`, `ainvoke_skill()`)
- ✅ Multi-source discovery (project, Anthropic config, plugins, custom paths)
- ✅ Plugin integration with MCPB manifest support
- ✅ Nested directory structures (up to 5 levels deep)
- ✅ Fully qualified skill names for conflict resolution
- ✅ Secure file path resolution with traversal prevention
- ✅ LangChain async integration (`ainvoke`)
- ✅ Backward compatible with v0.1

### v0.3 (Released)
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
- ✅ Created `docs/` folder with basic documentation

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
- Built with Python and Claude itself!
