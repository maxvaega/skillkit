# API Contract: Remove Tool Restriction Enforcement

**Feature**: Remove Tool Restriction Enforcement
**Version**: v0.3.0 (patch)
**Date**: 2025-11-30
**Contract Type**: Code Removal & Backward Compatibility

---

## Contract Overview

This contract defines the API changes for removing tool restriction enforcement while maintaining backward compatibility. All public APIs remain unchanged except for the removal of `ToolRestrictionError` exception class.

---

## Public API Changes

### 1. Exception Classes (BREAKING)

#### ToolRestrictionError (REMOVED)

**Module**: `skillkit.core.exceptions`

**Before** (v0.3.0):
```python
from skillkit.core.exceptions import ToolRestrictionError

try:
    executor.execute(script_path, args, skill_base_dir, metadata)
except ToolRestrictionError as e:
    print(f"Tool restriction error: {e}")
```

**After** (v0.3.0 patch):
```python
# ToolRestrictionError no longer exists - remove import and exception handling
# Script execution will never raise this exception

result = executor.execute(script_path, args, skill_base_dir, metadata)
```

**Breaking Change**: Yes
- Code importing `ToolRestrictionError` will get `ImportError`
- Code catching this exception should remove the handler

**Migration**:
```python
# BEFORE
from skillkit.core.exceptions import (
    PathSecurityError,
    ScriptPermissionError,
    ToolRestrictionError,  # ❌ Remove this import
    InterpreterNotFoundError
)

try:
    result = executor.execute(...)
except ToolRestrictionError:  # ❌ Remove this handler
    handle_restriction_error()
except PathSecurityError:
    handle_path_error()

# AFTER
from skillkit.core.exceptions import (
    PathSecurityError,
    ScriptPermissionError,
    # ToolRestrictionError removed
    InterpreterNotFoundError
)

try:
    result = executor.execute(...)
# ToolRestrictionError handler removed - scripts always execute
except PathSecurityError:
    handle_path_error()
```

---

### 2. SkillMetadata (NO CHANGES)

**Module**: `skillkit.core.models`

**Contract**: `allowed_tools` field remains unchanged

**Before** (v0.3.0):
```python
@dataclass(frozen=True, slots=True)
class SkillMetadata:
    name: str
    description: str
    skill_path: Path
    allowed_tools: tuple[str, ...] = field(default_factory=tuple)
```

**After** (v0.3.0 patch):
```python
# Identical - no changes
@dataclass(frozen=True, slots=True)
class SkillMetadata:
    name: str
    description: str
    skill_path: Path
    allowed_tools: tuple[str, ...] = field(default_factory=tuple)  # ✅ Preserved
```

**Breaking Change**: No
- Field remains accessible
- YAML parsing continues to work
- No enforcement happens (behavior change, not API change)

**Example Usage** (continues to work):
```python
# Reading allowed-tools field (still works)
metadata = skill_manager.get_skill("my-skill").metadata
if metadata.allowed_tools:
    print(f"Allowed tools: {metadata.allowed_tools}")

# Script execution (now always succeeds, regardless of allowed-tools)
result = skill_manager.execute_skill_script("my-skill", "script.py", {})
```

---

### 3. ScriptExecutor.execute() (BEHAVIORAL CHANGE, NO API CHANGE)

**Module**: `skillkit.core.scripts`

**Signature**: Unchanged

**Before** (v0.3.0):
```python
def execute(
    self,
    script_path: Path,
    arguments: ScriptArguments,
    skill_base_dir: Path,
    skill_metadata: "SkillMetadata",
) -> ScriptExecutionResult:
    """Execute a script with security controls.

    Raises:
        PathSecurityError: If path validation fails
        ScriptPermissionError: If script has dangerous permissions
        ToolRestrictionError: If 'Bash' not in allowed_tools  # ← REMOVED
        InterpreterNotFoundError: If interpreter not found
        ArgumentSerializationError: If arguments cannot be serialized
        ArgumentSizeError: If arguments too large
    """
```

**After** (v0.3.0 patch):
```python
def execute(
    self,
    script_path: Path,
    arguments: ScriptArguments,
    skill_base_dir: Path,
    skill_metadata: "SkillMetadata",
) -> ScriptExecutionResult:
    """Execute a script with security controls.

    Raises:
        PathSecurityError: If path validation fails
        ScriptPermissionError: If script has dangerous permissions
        # ToolRestrictionError removed
        InterpreterNotFoundError: If interpreter not found
        ArgumentSerializationError: If arguments cannot be serialized
        ArgumentSizeError: If arguments too large
    """
```

**Breaking Change**: No (API signature unchanged)
- Method signature identical
- Return type identical
- Behavioral change: No longer raises `ToolRestrictionError`

**Behavioral Change**:
```python
# Skill with allowed-tools: [Read, Write] (no Bash)

# BEFORE (v0.3.0):
try:
    result = executor.execute(script_path, {}, skill_base_dir, metadata)
except ToolRestrictionError:
    print("Script execution blocked by tool restrictions")

# AFTER (v0.3.0 patch):
result = executor.execute(script_path, {}, skill_base_dir, metadata)
# No exception raised - script executes successfully
```

---

## Private API Changes (NON-BREAKING)

### ScriptExecutor._check_tool_restrictions() (REMOVED)

**Module**: `skillkit.core.scripts`

**Status**: Private method removed

**Impact**: Non-breaking
- Private methods (prefix with `_`) are not part of public API
- External code should not be calling this method
- If called: `AttributeError: 'ScriptExecutor' object has no attribute '_check_tool_restrictions'`

---

## LangChain Integration Changes

### StructuredTool Creation (NO CHANGES)

**Module**: `skillkit.integrations.langchain`

**Contract**: Script tools continue to work identically

**Before** (v0.3.0):
```python
# Script tool creation for skill with allowed-tools: [Read, Write]
tools = manager.get_langchain_tools()
# Raises ToolRestrictionError when tool is invoked (if script executed)
```

**After** (v0.3.0 patch):
```python
# Script tool creation for skill with allowed-tools: [Read, Write]
tools = manager.get_langchain_tools()
# Tools created successfully, invocation executes scripts without restriction check
```

**Breaking Change**: No
- Tool creation API unchanged
- Tool invocation API unchanged
- Behavioral change: Scripts execute without tool restriction validation

---

## YAML Parsing Contract (NO CHANGES)

### SKILL.md Frontmatter

**Parser Module**: `skillkit.core.parser`

**Contract**: `allowed-tools` field continues to be parsed

**Before** (v0.3.0):
```yaml
---
name: pdf-extractor
description: Extract text from PDFs
allowed-tools:
  - Bash
  - Read
---
```

**After** (v0.3.0 patch):
```yaml
# Identical YAML - parsing unchanged
---
name: pdf-extractor
description: Extract text from PDFs
allowed-tools:
  - Bash
  - Read
---
```

**Parsing Behavior**:
```python
# BEFORE and AFTER (identical):
skill = manager.get_skill("pdf-extractor")
print(skill.metadata.allowed_tools)  # ('Bash', 'Read')
```

**Breaking Change**: No
- YAML structure unchanged
- Parsing logic unchanged
- Field populated in SkillMetadata

---

## Error Handling Contract Changes

### Exception Hierarchy (MODIFIED)

**Before** (v0.3.0):
```text
SkillsUseError
└── SkillSecurityError
    ├── PathSecurityError          ✅ Kept
    ├── SuspiciousInputError       ✅ Kept
    ├── SizeLimitExceededError     ✅ Kept
    └── ToolRestrictionError       ❌ Removed

SkillsUseError
└── ScriptError
    ├── InterpreterNotFoundError       ✅ Kept
    ├── ScriptNotFoundError            ✅ Kept
    ├── ScriptPermissionError          ✅ Kept
    ├── ArgumentSerializationError     ✅ Kept
    └── ArgumentSizeError              ✅ Kept
```

**After** (v0.3.0 patch):
```text
SkillsUseError
└── SkillSecurityError
    ├── PathSecurityError          ✅ Kept
    ├── SuspiciousInputError       ✅ Kept
    └── SizeLimitExceededError     ✅ Kept
    # ToolRestrictionError removed

SkillsUseError
└── ScriptError
    ├── InterpreterNotFoundError       ✅ Kept
    ├── ScriptNotFoundError            ✅ Kept
    ├── ScriptPermissionError          ✅ Kept
    ├── ArgumentSerializationError     ✅ Kept
    └── ArgumentSizeError              ✅ Kept
```

**Catch-all Exception Handling**:
```python
# Code catching parent exceptions continues to work
try:
    result = executor.execute(...)
except SkillSecurityError as e:  # ✅ Still works (PathSecurityError, SuspiciousInputError)
    handle_security_error(e)
except ScriptError as e:  # ✅ Still works (all Script* exceptions)
    handle_script_error(e)
except SkillsUseError as e:  # ✅ Still works (all library errors)
    handle_library_error(e)
```

---

## Backward Compatibility Summary

| Component | API Change | Backward Compatible | Migration Required |
|-----------|------------|--------------------|--------------------|
| `SkillMetadata.allowed_tools` | None | ✅ Yes | No |
| `ScriptExecutor.execute()` signature | None | ✅ Yes | No |
| `ScriptExecutor.execute()` behavior | More permissive | ✅ Yes | No (improvement) |
| `ToolRestrictionError` class | Deleted | ❌ No | Yes - remove imports |
| `_check_tool_restrictions()` method | Deleted | ✅ Yes | No (private API) |
| YAML parsing | None | ✅ Yes | No |
| LangChain integration | None | ✅ Yes | No |
| Other exception classes | None | ✅ Yes | No |

---

## Migration Guide

### For Library Users

**Step 1**: Remove `ToolRestrictionError` imports
```diff
from skillkit.core.exceptions import (
    PathSecurityError,
    ScriptPermissionError,
-   ToolRestrictionError,
    InterpreterNotFoundError
)
```

**Step 2**: Remove exception handlers for `ToolRestrictionError`
```diff
try:
    result = executor.execute(script_path, args, skill_base_dir, metadata)
-except ToolRestrictionError:
-    print("Script blocked by tool restrictions")
except PathSecurityError:
    print("Path security error")
```

**Step 3**: Update error handling documentation
```diff
# Error handling for script execution:
-# - ToolRestrictionError: Skill's allowed-tools doesn't include Bash
# - PathSecurityError: Path traversal attempt
# - ScriptPermissionError: Script has setuid/setgid
```

### For Skill Authors

**No changes required**:
- SKILL.md files with `allowed-tools` continue to work
- Scripts execute regardless of `allowed-tools` value
- No YAML schema changes

### For Framework Integrators

**LangChain Integration**:
```diff
# src/skillkit/integrations/langchain.py
# Update exception documentation in comments:
-# Possible exceptions: PathSecurityError, ToolRestrictionError, etc.
+# Possible exceptions: PathSecurityError, ScriptPermissionError, etc.
```

**Custom Integrations**:
- No API changes for public methods
- If catching `ToolRestrictionError`: Remove exception handler
- If checking `allowed_tools` field: Continues to work

---

## Testing Contract

### Test Assertions (CHANGED)

**Before** (v0.3.0):
```python
# Test that ToolRestrictionError is raised
def test_tool_restriction_enforcement():
    metadata = SkillMetadata(
        name="test",
        description="Test",
        skill_path=path,
        allowed_tools=("Read",)  # No Bash
    )
    executor = ScriptExecutor()
    with pytest.raises(ToolRestrictionError):
        executor.execute(script_path, {}, skill_base_dir, metadata)
```

**After** (v0.3.0 patch):
```python
# Test that scripts execute regardless of allowed-tools
def test_script_execution_ignores_allowed_tools():
    metadata = SkillMetadata(
        name="test",
        description="Test",
        skill_path=path,
        allowed_tools=("Read",)  # No Bash - should still execute
    )
    executor = ScriptExecutor()
    result = executor.execute(script_path, {}, skill_base_dir, metadata)
    assert result.exit_code == 0  # Should succeed
```

---

## Version Compatibility Matrix

| Component | v0.2.x | v0.3.0 (current) | v0.3.0 patch (this change) |
|-----------|--------|------------------|---------------------------|
| `allowed-tools` field | ✅ Exists | ✅ Exists | ✅ Exists |
| Tool restriction enforcement | ❌ N/A | ✅ Enforced | ❌ Removed |
| `ToolRestrictionError` | ❌ N/A | ✅ Exists | ❌ Removed |
| Script execution | ❌ N/A | ✅ Works | ✅ Works (more permissive) |

---

## Summary

**Public API Changes**:
- ❌ **BREAKING**: `ToolRestrictionError` exception class removed
- ✅ **COMPATIBLE**: All other APIs unchanged

**Behavioral Changes**:
- Scripts now execute regardless of `allowed-tools` value
- More permissive behavior (previously blocked scripts now succeed)

**Migration Effort**:
- Low: Remove import and exception handler (if present)
- Most code unaffected (if not using `ToolRestrictionError`)

**Recommended Version Bump**: v0.3.x (patch/minor) - not v1.0.0
- No breaking changes to core APIs (`SkillMetadata`, `ScriptExecutor.execute()`)
- Breaking change limited to exception class (minor breaking change acceptable in patch)
