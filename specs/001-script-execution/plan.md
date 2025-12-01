# Implementation Plan: Tool ID Format Update for Script Execution

**Branch**: `001-script-execution` | **Date**: 2025-01-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-script-execution/spec.md`

**Note**: This plan focuses on updating the tool naming format from `skill_name.script_name` (dot separator) to `skill-name__script_name` (double underscore) with validation to ensure LLM provider compatibility.

## Summary

The script execution feature (v0.3.0) has been fully implemented, but the tool ID format needs to be updated before release. The specification was clarified (Session 2025-12-01) to require:

- **Format**: `skill-name__script-name` (lowercase with double underscore separator)
- **Validation**: Regex `^[a-z0-9-]+__[a-z0-9_]+$` with max 60 characters
- **Rationale**: LLM provider compatibility (some providers have issues with dot separators in tool IDs)

The current implementation uses `skill_name.script_name` format. This plan addresses updating the format across:
1. Core logic in `src/skillkit/core/scripts.py` (ScriptMetadata.get_fully_qualified_name)
2. LangChain integration in `src/skillkit/integrations/langchain.py`
3. All test files referencing the old format
4. Documentation in README.md and examples

## Technical Context

**Language/Version**: Python 3.10+ (existing skillkit v0.3.0 minimum requirement)
**Primary Dependencies**: PyYAML 6.0+, aiofiles 23.0+, subprocess (stdlib), pathlib (stdlib), re (stdlib)
**Storage**: Filesystem-based (scripts stored in skill directories: `scripts/` or skill root)
**Testing**: pytest 7.0+, pytest-cov 4.0+ (existing test infrastructure)
**Target Platform**: Linux, macOS, Windows (cross-platform via subprocess module)
**Project Type**: Single Python library
**Performance Goals**: No performance impact (format change only, validation adds <1ms overhead)
**Constraints**: Backward compatibility NOT required (new feature in v0.3.0, no existing deployments)
**Scale/Scope**: 5 core files, ~15 test files, 2 documentation files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**No constitution violations detected**: This project does not have a constitution file configured. The changes follow existing skillkit architecture patterns and Python library best practices.

## Project Structure

### Documentation (this feature)

```text
specs/001-script-execution/
├── spec.md                  # Feature specification (UPDATED with tool ID requirements)
├── plan.md                  # This file (/speckit.plan command output)
├── research.md              # Phase 0 output (tool ID validation research)
├── data-model.md            # Phase 1 output (ToolIDValidationError exception design)
├── quickstart.md            # Phase 1 output (usage examples with new format)
├── contracts/               # Phase 1 output (API contracts for validation)
└── tasks.md                 # Phase 2 output (/speckit.tasks command - NOT created yet)
```

### Source Code (repository root)

```text
src/skillkit/
├── core/
│   ├── scripts.py           # UPDATE: ScriptMetadata.get_fully_qualified_name() method
│   │                        #         Add validate_tool_id() function
│   └── exceptions.py        # ADD: ToolIDValidationError exception class
├── integrations/
│   └── langchain.py         # UPDATE: Tool name creation and validation
└── __init__.py              # ADD: Export ToolIDValidationError

tests/
├── test_scripts.py          # UPDATE: Test cases for new format and validation
├── test_langchain.py        # UPDATE: Test cases for LangChain integration
├── test_script_langchain_integration.py  # UPDATE: Integration test assertions
└── fixtures/
    └── skills/              # Test skills (scripts already exist)

examples/
├── script_execution.py      # ADD: New example demonstrating script tool usage
└── README.md                # UPDATE: Documentation with new tool ID format

README.md                    # UPDATE: Script execution section with format details
```

**Structure Decision**: Single project structure (Option 1). All changes are within the existing skillkit library source tree (`src/skillkit/`), matching the established pattern for the v0.1 and v0.2 releases.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected - this section is not applicable.

## Phase 0: Research & Design Decisions

### Research Tasks

1. **Tool ID Validation Pattern Research**
   - Research LLM provider tool ID requirements (Anthropic, OpenAI, Google)
   - Validate regex pattern `^[a-z0-9-]+__[a-z0-9_]+$` against provider specs
   - Document rationale for 60-character limit
   - Research Python regex performance for validation

2. **Exception Hierarchy Research**
   - Review existing skillkit exception hierarchy
   - Determine parent class for ToolIDValidationError (likely SkillkitError)
   - Document error message format and required context fields

3. **Backward Compatibility Analysis**
   - Confirm no existing deployments use script tools (v0.3.0 is new feature)
   - Document migration strategy (none needed - new feature)
   - Verify test fixtures don't rely on old format

### Key Decisions

**Decision 1: Validation Timing**
- **When**: Validate tool IDs during tool registration (in `create_script_tools()`)
- **Rationale**: Fail fast at tool creation time, not during agent execution
- **Alternative Rejected**: Validate during script execution (too late, poor error UX)

**Decision 2: Error Handling Strategy**
- **Approach**: Raise ToolIDValidationError with descriptive message including invalid ID
- **Rationale**: Clear, actionable error messages for skill authors
- **Alternative Rejected**: Log warning and skip tool (silent failure is bad UX)

**Decision 3: Format Enforcement**
- **Approach**: Automatically lowercase skill and script names before formatting
- **Rationale**: Skills may have mixed-case names in SKILL.md
- **Alternative Rejected**: Reject mixed-case names (breaking change for existing skills)

## Phase 1: Design Artifacts

### Data Model Changes

**New Exception Class**: `ToolIDValidationError`
```python
class ToolIDValidationError(SkillkitError):
    """Tool ID failed validation (invalid format or exceeded 60 character limit).

    Attributes:
        tool_id: The invalid tool ID that failed validation
        skill_name: Original skill name before formatting
        script_name: Original script name before formatting
        reason: Specific reason for validation failure
    """
    def __init__(self, message: str, tool_id: str, skill_name: str,
                 script_name: str, reason: str):
        super().__init__(message)
        self.tool_id = tool_id
        self.skill_name = skill_name
        self.script_name = script_name
        self.reason = reason
```

**Updated Method**: `ScriptMetadata.get_fully_qualified_name()`
```python
def get_fully_qualified_name(self, skill_name: str) -> str:
    """Generate fully qualified tool name with validation.

    Format: {lowercase-skill-name}__{lowercase-script-name}
    Validation: ^[a-z0-9-]+__[a-z0-9_]+$ (max 60 chars)

    Args:
        skill_name: Skill name from metadata

    Returns:
        Validated tool ID string

    Raises:
        ToolIDValidationError: If generated ID fails validation
    """
    # Lowercase and replace underscores with hyphens in skill name
    skill_part = skill_name.lower().replace('_', '-')

    # Lowercase script name (keep underscores)
    script_part = self.name.lower()

    # Generate tool ID
    tool_id = f"{skill_part}__{script_part}"

    # Validate format and length
    validate_tool_id(tool_id, skill_name, self.name)

    return tool_id
```

**New Validation Function**: `validate_tool_id()`
```python
def validate_tool_id(tool_id: str, skill_name: str, script_name: str) -> None:
    """Validate tool ID format and length.

    Requirements:
    - Format: ^[a-z0-9-]+__[a-z0-9_]+$ (lowercase, digits, hyphens in skill part,
              underscores in script part, double underscore separator)
    - Length: Maximum 60 characters total

    Args:
        tool_id: Generated tool ID to validate
        skill_name: Original skill name (for error context)
        script_name: Original script name (for error context)

    Raises:
        ToolIDValidationError: If validation fails
    """
    import re

    # Check length
    if len(tool_id) > 60:
        raise ToolIDValidationError(
            f"Tool ID exceeds 60 character limit: '{tool_id}' ({len(tool_id)} chars)",
            tool_id=tool_id,
            skill_name=skill_name,
            script_name=script_name,
            reason="length_exceeded"
        )

    # Check format
    pattern = r'^[a-z0-9-]+__[a-z0-9_]+$'
    if not re.match(pattern, tool_id):
        raise ToolIDValidationError(
            f"Tool ID has invalid format: '{tool_id}'. "
            f"Must match pattern: ^[a-z0-9-]+__[a-z0-9_]+$ "
            f"(lowercase skill name with hyphens/digits + '__' + "
            f"lowercase script name with underscores/digits)",
            tool_id=tool_id,
            skill_name=skill_name,
            script_name=script_name,
            reason="invalid_format"
        )
```

### API Contracts

**Contract 1: Tool ID Generation**
```yaml
operation: ScriptMetadata.get_fully_qualified_name
inputs:
  skill_name: string (any case, may contain underscores/hyphens/digits)
outputs:
  tool_id: string (validated format ^[a-z0-9-]+__[a-z0-9_]+$, max 60 chars)
errors:
  - ToolIDValidationError (invalid format or length exceeded)
side_effects: none
examples:
  - input: {skill_name: "PDF-Extractor", script_name: "extract_text"}
    output: "pdf-extractor__extract_text"
  - input: {skill_name: "csv_parser", script_name: "parse"}
    output: "csv-parser__parse"
  - input: {skill_name: "VeryLongSkillNameThatExceedsLimit", script_name: "script"}
    error: ToolIDValidationError (length_exceeded)
```

**Contract 2: Validation Function**
```yaml
operation: validate_tool_id
inputs:
  tool_id: string
  skill_name: string (original, for context)
  script_name: string (original, for context)
outputs: none (raises on failure)
errors:
  - ToolIDValidationError (invalid_format | length_exceeded)
side_effects: none
examples:
  - input: {tool_id: "pdf-extractor__extract", skill_name: "PDF-Extractor", script_name: "extract"}
    output: null (success)
  - input: {tool_id: "pdf.extractor__extract", skill_name: "pdf.extractor", script_name: "extract"}
    error: ToolIDValidationError (invalid_format, contains dot)
  - input: {tool_id: "PDF-Extractor__Extract", skill_name: "PDF-Extractor", script_name: "Extract"}
    error: ToolIDValidationError (invalid_format, uppercase letters)
```

### Quickstart Example

```python
"""Script execution with new tool ID format (v0.3.0+)."""

from skillkit import SkillManager
from skillkit.integrations.langchain import create_langchain_tools

# Initialize manager and discover skills
manager = SkillManager()
manager.discover()

# Create LangChain tools (includes script tools)
tools = create_langchain_tools(manager)

# Print generated tool IDs
for tool in tools:
    print(f"Tool: {tool.name}")
    # Examples:
    # - "pdf-extractor" (prompt-based tool)
    # - "pdf-extractor__extract" (script tool)
    # - "pdf-extractor__convert" (script tool)
    # - "csv-parser__parse" (script tool)

# Use with LangChain agent
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
agent = create_react_agent(llm, tools)
executor = AgentExecutor(agent=agent, tools=tools)

# Agent can now invoke script tools with validated IDs
result = executor.invoke({
    "input": "Extract text from document.pdf using pdf-extractor__extract"
})
```

## Phase 2: Implementation Tasks

Tasks will be generated in `tasks.md` by the `/speckit.tasks` command. Key implementation areas:

1. **Core Module Updates** (`src/skillkit/core/scripts.py`)
   - Add `validate_tool_id()` function
   - Update `ScriptMetadata.get_fully_qualified_name()` method
   - Add unit tests for validation logic

2. **Exception Hierarchy** (`src/skillkit/core/exceptions.py`)
   - Add `ToolIDValidationError` exception class
   - Export in `__init__.py`
   - Add exception tests

3. **LangChain Integration** (`src/skillkit/integrations/langchain.py`)
   - Update tool name generation to use new format
   - Add error handling for validation failures
   - Update integration tests

4. **Test Suite Updates**
   - Update all test assertions expecting old format (`skill_name.script_name`)
   - Add validation test cases (valid/invalid formats, length limits)
   - Update integration tests

5. **Documentation Updates**
   - Update README.md with new format and validation requirements
   - Add example in `examples/script_execution.py`
   - Update docstrings in affected modules

## Success Criteria

- All tool IDs generated match regex `^[a-z0-9-]+__[a-z0-9_]+$`
- All tool IDs are ≤60 characters
- ToolIDValidationError raised for invalid formats with clear error messages
- All existing tests pass with updated assertions
- Documentation accurately reflects new format
- No backward compatibility issues (confirmed: new feature, no existing deployments)

## Notes

- **No migration needed**: Script execution is new in v0.3.0, no existing deployments to migrate
- **Performance impact**: Validation adds <1ms overhead per tool registration (negligible)
- **LangChain compatibility**: StructuredTool accepts any string for `name` parameter, format is our choice
- **Future consideration**: If tool ID collisions occur across skills, consider adding skill source prefix
