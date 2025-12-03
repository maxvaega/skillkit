# LangChain Integration

This guide covers how to integrate skillkit with LangChain agents.

## Table of Contents

- [Basic Integration (Sync)](#basic-integration-sync)
- [Async Integration](#async-integration)
- [Script Tool Integration](#script-tool-integration)
- [Tool ID Format and Validation](#tool-id-format-and-validation)
- [Complete Examples](#complete-examples)

---

## Basic Integration (Sync)

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

---

## Async Integration

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

---

## Script Tool Integration

Scripts are automatically exposed as separate LangChain tools when you use `create_langchain_tools()`:

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

### How It Works

1. **Automatic Detection**: During `discover()`, skillkit recursively scans for scripts in skill directories
2. **Tool Creation**: Each script is exposed as a separate `StructuredTool` with its own name and description
3. **Agent Access**: LangChain agents can invoke scripts like any other tool
4. **Parameter Handling**: LLM-generated parameters are automatically normalized to lowercase before execution

---

## Tool ID Format and Validation

Script tool IDs follow a validated format to ensure LLM provider compatibility:

### Format Rules

- **Format**: `{skill-name}__{script-name}` (double underscore separator)
- **Validation Pattern**: `^[a-z0-9-]+__[a-z0-9_]+$`
- **Max Length**: 60 characters
- **Automatic Normalization**:
  - Skill names: Lowercase with underscores converted to hyphens
  - Script names: Lowercase with underscores preserved

### Examples

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
from skillkit.core.exceptions import ToolIDValidationError

try:
    tools = create_langchain_tools(manager)
except ToolIDValidationError as e:
    print(f"Invalid tool ID: {e}")
```

---

## Complete Examples

### Example 1: Basic Agent with Skills

See `examples/langchain_agent.py` for a complete working example:

```python
from skillkit import SkillManager
from skillkit.integrations.langchain import create_langchain_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# Setup
manager = SkillManager()
manager.discover()
tools = create_langchain_tools(manager)

# Create agent
llm = ChatOpenAI(model="gpt-4")
agent = create_agent(llm, tools, system_prompt="You are a helpful assistant.")

# Run query
result = agent.invoke({"messages": [{"role": "user", "content": "Review my code"}]})
```

### Example 2: Async Agent with Script Tools

See `examples/async_usage.py` for async patterns:

```python
import asyncio
from skillkit import SkillManager
from skillkit.integrations.langchain import create_langchain_tools

async def main():
    manager = SkillManager()
    await manager.adiscover()

    tools = create_langchain_tools(manager)
    # Tools now include both skill invocation and script execution tools

    # Use with async LangChain agent...

asyncio.run(main())
```

### Example 3: Error Handling

```python
from skillkit import SkillNotFoundError, ContentLoadError
from skillkit.core.exceptions import ScriptNotFoundError

try:
    tools = create_langchain_tools(manager)
    result = agent.invoke({"messages": [...]})
except SkillNotFoundError:
    print("Skill not found during tool creation")
except ContentLoadError:
    print("Skill file is unreadable")
except ScriptNotFoundError:
    print("Script not found in skill directory")
```

---

## Best Practices

1. **Discover Once**: Call `discover()` once at startup and reuse the manager
2. **Async When Possible**: Use `adiscover()` and `ainvoke()` for better performance
3. **Monitor Cache**: Use `manager.get_cache_stats()` to verify good cache hit rates
4. **Handle Errors**: Always wrap agent invocations in try-except blocks
5. **Tool Descriptions**: Ensure SKILL.md descriptions are clear for LLM understanding
6. **Script Parameters**: Use lowercase parameter names in scripts for consistency

---

## Additional Resources

- **Basic Usage**: See `examples/basic_usage.py`
- **Async Patterns**: See `examples/async_usage.py`
- **LangChain Agent**: See `examples/langchain_agent.py`
- **Script Execution**: See [Core Features - Script Execution](../core-features.md#script-execution)
- **Debugging**: See [Core Features - Debugging Tips](../core-features.md#debugging-tips)
