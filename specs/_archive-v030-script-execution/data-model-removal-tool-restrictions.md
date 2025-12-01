# Data Model Changes: Remove Tool Restriction Enforcement

**Feature**: Remove Tool Restriction Enforcement
**Version**: v0.3.0 (patch)
**Date**: 2025-11-30

---

## Overview

This document defines the changes to existing data models for removing tool restriction enforcement. The primary goal is to preserve backward compatibility while removing enforcement logic.

---

## Modified Data Models

### 1. SkillMetadata (NO CHANGES TO STRUCTURE)

**Location**: `src/skillkit/core/models.py:60-88`

**Current State**:
```python
@dataclass(frozen=True, slots=True)
class SkillMetadata:
    """Lightweight skill metadata loaded during discovery phase."""

    name: str
    description: str
    skill_path: Path
    allowed_tools: tuple[str, ...] = field(default_factory=tuple)  # ← KEEP THIS FIELD
```

**Change**: **NONE** - Field remains for backward compatibility

**Rationale**:
- Existing SKILL.md files may have `allowed-tools` in frontmatter
- Users may read `skill.metadata.allowed_tools` in their code
- Removing would be a breaking change (requires major version bump)
- Spec clarification (2025-11-30, Q5): "Keep allowed-tools field in SkillMetadata for compatibility but remove all code that checks/enforces it"

**Impact**:
- ✅ Backward compatible - no API changes
- ✅ Parsing continues to work (test_parser.py, test_models.py remain)
- ✅ Field accessible but not enforced

---

### 2. ScriptExecutor (METHOD REMOVED)

**Location**: `src/skillkit/core/scripts.py:833-869`

**Current State** (TO BE REMOVED):
```python
class ScriptExecutor:
    """Execute scripts with security controls and timeout enforcement."""

    def _check_tool_restrictions(self, skill_metadata: "SkillMetadata") -> None:
        """Check if script execution is allowed based on skill's tool restrictions.

        Args:
            skill_metadata: SkillMetadata instance containing allowed_tools

        Raises:
            ToolRestrictionError: If 'Bash' not in allowed_tools (when restrictions exist)
        """
        from skillkit.core.exceptions import ToolRestrictionError

        # Handle None/empty allowed_tools (no restrictions)
        if not skill_metadata.allowed_tools:
            return

        # Check if 'Bash' is in allowed tools
        if "Bash" not in skill_metadata.allowed_tools:
            allowed_tools_str = ", ".join(skill_metadata.allowed_tools)
            raise ToolRestrictionError(
                f"Script execution not allowed for skill '{skill_metadata.name}'. "
                f"The skill's allowed-tools list does not include 'Bash'. "
                f"Allowed tools: [{allowed_tools_str}]"
            )
```

**Change**: **DELETE METHOD ENTIRELY**

**Modified execute() method** (line 1134):
```python
# BEFORE (line 1134):
self._check_tool_restrictions(skill_metadata)

# AFTER:
# (line removed entirely)
```

**Rationale**:
- Method only used for tool restriction enforcement
- No other call sites exist
- Spec clarification (2025-11-30): Complete removal

**Impact**:
- ✅ Scripts execute regardless of `allowed-tools` value
- ✅ No security regression (wasn't a security boundary)
- ✅ Minor performance improvement (eliminates conditional check)

---

## Removed Exception Classes

### ToolRestrictionError (DELETED)

**Location**: `src/skillkit/core/exceptions.py:427-461`

**Current State** (TO BE REMOVED):
```python
class ToolRestrictionError(SkillSecurityError):
    """Raised when tool restrictions prevent script execution.

    This exception is raised when a skill's allowed-tools list does not
    include 'Bash', which is required for script execution.

    Attributes:
        skill_name: Name of the skill with tool restrictions
        allowed_tools: List of allowed tools (may be empty)
    """

    def __init__(
        self,
        message: str,
        skill_name: str | None = None,
        allowed_tools: List[str] | None = None,
    ) -> None:
        super().__init__(message)
        self.skill_name = skill_name
        self.allowed_tools = allowed_tools or []
```

**Change**: **DELETE CLASS ENTIRELY**

**Rationale**:
- Only used by `_check_tool_restrictions()` method
- No other code paths raise this exception
- Spec clarification (2025-11-30, Q2): "Remove ToolRestrictionError exception class entirely"

**Impact**:
- ⚠️ Code catching `ToolRestrictionError` will get `ImportError` - MUST UPDATE:
  - `examples/script_execution.py:26` - Remove import
  - `README.md:442, 456` - Remove from error handling examples
  - `tests/test_script_executor.py:420` - Remove test case
  - `tests/test_script_executor_phase6.py` - Delete entire file

---

## Unchanged Data Models

### 1. ScriptMetadata

**Location**: `src/skillkit/core/scripts.py:77-143`

**Change**: **NONE**

**Rationale**: No tool restriction logic in ScriptMetadata

---

### 2. ScriptExecutionResult

**Location**: `src/skillkit/core/scripts.py:145-274`

**Change**: **NONE**

**Rationale**: No tool restriction logic in ScriptExecutionResult

---

### 3. All Other Exception Classes

**Location**: `src/skillkit/core/exceptions.py`

**Change**: **NONE** (except ToolRestrictionError deletion)

**Preserved Classes**:
- ✅ PathSecurityError - Still used for path validation
- ✅ ScriptPermissionError - Still used for setuid/setgid checks
- ✅ InterpreterNotFoundError - Still used for interpreter validation
- ✅ ArgumentSerializationError - Still used for JSON serialization
- ✅ ArgumentSizeError - Still used for size limit enforcement
- ✅ All other exception classes remain

---

## Entity Relationships (After Changes)

```text
SkillMetadata
├── allowed_tools: tuple[str, ...]  ← FIELD PRESERVED (not enforced)
└── (parsed from YAML frontmatter)

ScriptExecutor
├── execute() method
│   ├── _validate_script_path()     ✅ KEPT (security control)
│   ├── _check_permissions()        ✅ KEPT (security control)
│   ├── _check_tool_restrictions()  ❌ REMOVED
│   ├── _resolve_interpreter()      ✅ KEPT
│   ├── _build_environment()        ✅ KEPT
│   └── _execute_subprocess()       ✅ KEPT
└── Other security controls remain intact

Exceptions
├── PathSecurityError               ✅ KEPT
├── ScriptPermissionError           ✅ KEPT
├── InterpreterNotFoundError        ✅ KEPT
├── ArgumentSerializationError      ✅ KEPT
├── ArgumentSizeError               ✅ KEPT
└── ToolRestrictionError            ❌ REMOVED
```

---

## Migration Impact Analysis

### For End Users

**Scenario 1**: Skill with `allowed-tools: [Read, Write]` (Bash not included)
- **Before**: Script execution raises `ToolRestrictionError`
- **After**: Script executes successfully
- **Impact**: ✅ Improvement (fewer errors)

**Scenario 2**: Skill with `allowed-tools: [Bash, Read]` (Bash included)
- **Before**: Script execution succeeds
- **After**: Script execution succeeds
- **Impact**: ✅ No change (same behavior)

**Scenario 3**: Skill with no `allowed-tools` field
- **Before**: Script execution succeeds (no restrictions)
- **After**: Script execution succeeds
- **Impact**: ✅ No change (same behavior)

**Scenario 4**: Code catching `ToolRestrictionError`
- **Before**: Catches exception when Bash not in allowed-tools
- **After**: `ImportError` (class doesn't exist)
- **Impact**: ⚠️ **BREAKING** - Must remove exception handling

### For Library Integrators

**LangChain Integration**:
- **Location**: `src/skillkit/integrations/langchain.py:330`
- **Change**: Remove `ToolRestrictionError` from exception comment
- **Impact**: ✅ No functional change (no enforcement in LangChain layer)

**Custom Integrations**:
- If custom code imports `ToolRestrictionError`: ⚠️ **BREAKING** - Must remove import
- If custom code calls `_check_tool_restrictions()`: ⚠️ **BREAKING** - Private method removed
- If custom code reads `allowed_tools` field: ✅ No change (field preserved)

---

## Testing Changes Required

### Tests to DELETE

1. **`tests/test_script_executor_phase6.py`** - Entire file (150+ lines)
   - Reason: All tests validate `_check_tool_restrictions()` behavior
   - Methods: 7 test methods all focused on tool restriction enforcement

2. **`tests/test_script_executor.py:420`** - Single test case
   - Reason: Expects `ToolRestrictionError` to be raised
   - Replace with regression test verifying scripts execute regardless of allowed-tools

3. **`tests/fixtures/skills/restricted-skill/`** - Entire directory
   - Reason: Test fixture used exclusively for restriction testing

### Tests to KEEP

1. **`tests/test_parser.py`** - All allowed-tools parsing tests
   - Reason: Field still parsed from YAML (backward compatibility)

2. **`tests/test_models.py`** - All SkillMetadata tests
   - Reason: allowed_tools field remains in model

3. **All other `test_script_executor*.py` tests**
   - Reason: Test other security controls (path validation, permissions, timeout)

### New Tests to ADD

1. **Regression test**: Verify script execution succeeds with any `allowed-tools` value
   ```python
   def test_script_execution_ignores_allowed_tools():
       """Verify scripts execute regardless of allowed-tools field."""
       # Skill with allowed-tools that doesn't include Bash
       metadata = SkillMetadata(
           name="test-skill",
           description="Test",
           skill_path=skill_path,
           allowed_tools=("Read", "Write")  # No "Bash"
       )
       executor = ScriptExecutor()
       result = executor.execute(script_path, {}, skill_base_dir, metadata)
       assert result.exit_code == 0  # Should succeed, not raise error
   ```

---

## Backward Compatibility Guarantees

| Component | Change | Backward Compatible? | Notes |
|-----------|--------|---------------------|-------|
| `SkillMetadata.allowed_tools` | None | ✅ Yes | Field preserved |
| YAML parsing of `allowed-tools` | None | ✅ Yes | Continues to work |
| `ScriptExecutor.execute()` | Removed check | ✅ Yes | More permissive (scripts that failed now succeed) |
| `ToolRestrictionError` class | Deleted | ❌ No | Code importing this will break |
| `_check_tool_restrictions()` method | Deleted | ❌ No | Private method (breaking private API is acceptable) |

**Breaking Change Assessment**:
- **Public API**: No breaking changes (allowed_tools field preserved)
- **Exception Handling**: Breaking for code catching `ToolRestrictionError`
- **Recommendation**: Document as minor version patch (0.3.x) since it's a removal of validation, not a change to core API

---

## Documentation Updates Required

### 1. README.md
- Remove ToolRestrictionError from error handling examples (lines 442, 456)
- Update script execution section to reflect no tool restriction enforcement

### 2. examples/script_execution.py
- Remove `ToolRestrictionError` from imports (line 26)
- Remove exception handling for tool restrictions

### 3. Spec Documents
- ✅ spec.md - Already updated (FR-008 removed, Out of Scope section added)
- Update tasks.md - Remove T045-T047 tasks
- Update data-model.md - Remove ToolRestrictionError references (line 367)
- Update IMPLEMENTATION_GUIDE.md - Remove enforcement documentation (line 665)
- Update research-langchain-integration.md - Remove ToolRestrictionError class (line 588)

---

## Summary of Changes

**Deleted**:
1. `ScriptExecutor._check_tool_restrictions()` method (37 lines)
2. `ToolRestrictionError` exception class (35 lines)
3. `tests/test_script_executor_phase6.py` file (150+ lines)
4. `tests/fixtures/skills/restricted-skill/` directory
5. Multiple documentation references

**Modified**:
1. `ScriptExecutor.execute()` - Remove call to `_check_tool_restrictions()` (1 line)
2. `examples/script_execution.py` - Remove import and exception handling (2-3 lines)
3. `src/skillkit/integrations/langchain.py` - Remove exception from comment (1 line)
4. Documentation files - Remove references to enforcement

**Preserved**:
1. `SkillMetadata.allowed_tools` field (backward compatibility)
2. All YAML parsing logic for `allowed-tools`
3. All other ScriptExecutor security controls
4. All other exception classes

**Net Impact**: ~250 lines removed, 0 lines added, 100% backward compatible for public API
