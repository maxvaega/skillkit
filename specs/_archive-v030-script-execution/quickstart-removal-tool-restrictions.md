# Quickstart: Remove Tool Restriction Enforcement

**Feature**: Remove Tool Restriction Enforcement
**Version**: v0.3.0 (patch)
**Date**: 2025-11-30
**Estimated Time**: 2-3 hours

---

## Overview

This quickstart guide provides step-by-step instructions for removing tool restriction enforcement from skillkit v0.3.0. The work involves deleting code, removing tests, and updating documentation while preserving backward compatibility.

---

## Prerequisites

- Python 3.10+ environment with skillkit v0.3.0 installed
- pytest 7.0+ for running tests
- git for tracking changes
- Access to the skillkit repository on branch `001-script-execution`

---

## Step-by-Step Implementation

### Phase 1: Code Removal (30 minutes)

#### 1.1 Remove `_check_tool_restrictions()` method

**File**: `src/skillkit/core/scripts.py`

**Action**: Delete method (lines 833-869)

**Steps**:
```bash
# Open file
code src/skillkit/core/scripts.py

# Find method at line 833:
# def _check_tool_restrictions(self, skill_metadata: "SkillMetadata") -> None:

# Delete entire method including:
# - Docstring (lines 833-852)
# - Implementation (lines 853-869)
# - Total: 37 lines
```

**Verification**:
```bash
# Ensure method is removed
grep -n "_check_tool_restrictions" src/skillkit/core/scripts.py
# Should return only the call site (line 1134), not the definition
```

#### 1.2 Remove method call from `execute()`

**File**: `src/skillkit/core/scripts.py`

**Action**: Delete line 1134

**Steps**:
```bash
# Find line 1134:
# self._check_tool_restrictions(skill_metadata)

# Delete entire line
```

**Before**:
```python
# Check permissions
self._check_permissions(validated_path)

# Check tool restrictions (must be after path/permission validation)
self._check_tool_restrictions(skill_metadata)  # ← DELETE THIS LINE

# Resolve interpreter
interpreter = self._resolve_interpreter(validated_path)
```

**After**:
```python
# Check permissions
self._check_permissions(validated_path)

# Resolve interpreter
interpreter = self._resolve_interpreter(validated_path)
```

**Verification**:
```bash
# Ensure call is removed
grep -n "_check_tool_restrictions" src/skillkit/core/scripts.py
# Should return no results
```

#### 1.3 Remove `ToolRestrictionError` exception class

**File**: `src/skillkit/core/exceptions.py`

**Action**: Delete class (lines 427-461)

**Steps**:
```bash
# Open file
code src/skillkit/core/exceptions.py

# Find class at line 427:
# class ToolRestrictionError(SkillSecurityError):

# Delete entire class including:
# - Class definition and docstring (lines 427-443)
# - __init__ method (lines 445-461)
# - Total: 35 lines
```

**Verification**:
```bash
# Ensure class is removed
grep -n "ToolRestrictionError" src/skillkit/core/exceptions.py
# Should return no results
```

#### 1.4 Update LangChain integration

**File**: `src/skillkit/integrations/langchain.py`

**Action**: Remove `ToolRestrictionError` from comment (line 330)

**Steps**:
```bash
# Find line 330 (approximately):
# Comment mentions: PathSecurityError, ToolRestrictionError, etc.

# Update comment to remove ToolRestrictionError reference
```

**Before**:
```python
# Possible exceptions: PathSecurityError, ToolRestrictionError, etc.
```

**After**:
```python
# Possible exceptions: PathSecurityError, ScriptPermissionError, etc.
```

**Verification**:
```bash
# Ensure reference is removed
grep -n "ToolRestrictionError" src/skillkit/integrations/langchain.py
# Should return no results
```

---

### Phase 2: Test Removal (20 minutes)

#### 2.1 Delete `test_script_executor_phase6.py`

**File**: `tests/test_script_executor_phase6.py`

**Action**: Delete entire file

**Steps**:
```bash
# Delete file
rm tests/test_script_executor_phase6.py

# Verify deletion
ls tests/test_script_executor_phase6.py
# Should return: No such file or directory
```

#### 2.2 Remove test case from `test_script_executor.py`

**File**: `tests/test_script_executor.py`

**Action**: Remove ToolRestrictionError test case (line 420 and related)

**Steps**:
```bash
# Open file
code tests/test_script_executor.py

# Find line with ToolRestrictionError
grep -n "ToolRestrictionError" tests/test_script_executor.py

# Remove test method that uses ToolRestrictionError
# (Likely a test method expecting the exception to be raised)
```

**Verification**:
```bash
# Ensure reference is removed
grep -n "ToolRestrictionError" tests/test_script_executor.py
# Should return no results
```

#### 2.3 Delete `restricted-skill` fixture

**Directory**: `tests/fixtures/skills/restricted-skill/`

**Action**: Delete entire directory

**Steps**:
```bash
# Delete directory
rm -rf tests/fixtures/skills/restricted-skill/

# Verify deletion
ls tests/fixtures/skills/restricted-skill/
# Should return: No such file or directory
```

#### 2.4 Review other test files

**Files**: `tests/test_script_executor_phase3.py`, `tests/test_script_executor_phase4.py`

**Action**: Check for ToolRestrictionError references

**Steps**:
```bash
# Check phase3
grep -n "ToolRestrictionError" tests/test_script_executor_phase3.py

# Check phase4
grep -n "ToolRestrictionError" tests/test_script_executor_phase4.py

# If any references found, remove them
```

---

### Phase 3: Documentation Updates (40 minutes)

#### 3.1 Update README.md

**File**: `README.md`

**Action**: Remove ToolRestrictionError from examples (lines 442, 456)

**Steps**:
```bash
# Find references
grep -n "ToolRestrictionError" README.md

# Remove imports and exception handling examples
```

**Before** (line 442):
```python
from skillkit.core.exceptions import (
    PathSecurityError,
    ScriptPermissionError,
    ToolRestrictionError,
    InterpreterNotFoundError
)
```

**After**:
```python
from skillkit.core.exceptions import (
    PathSecurityError,
    ScriptPermissionError,
    InterpreterNotFoundError
)
```

**Before** (line 456):
```python
except ToolRestrictionError:
    print("Script execution not allowed (tool restrictions)")
```

**After**:
```python
# ToolRestrictionError removed - scripts execute regardless of allowed-tools
```

#### 3.2 Update examples/script_execution.py

**File**: `examples/script_execution.py`

**Action**: Remove import and exception handling (line 26)

**Steps**:
```bash
# Find references
grep -n "ToolRestrictionError" examples/script_execution.py

# Remove import and exception handler
```

**Before**:
```python
from skillkit.core.exceptions import (
    PathSecurityError,
    ScriptPermissionError,
    ToolRestrictionError,  # ← Remove
    InterpreterNotFoundError
)

try:
    result = executor.execute(...)
except ToolRestrictionError:  # ← Remove handler
    print("Tool restriction error")
except PathSecurityError:
    print("Path error")
```

**After**:
```python
from skillkit.core.exceptions import (
    PathSecurityError,
    ScriptPermissionError,
    InterpreterNotFoundError
)

try:
    result = executor.execute(...)
except PathSecurityError:
    print("Path error")
```

#### 3.3 Update spec documents

**Files**:
- `specs/001-script-execution/tasks.md`
- `specs/001-script-execution/data-model.md`
- `specs/001-script-execution/IMPLEMENTATION_GUIDE.md`
- `specs/001-script-execution/research-langchain-integration.md`

**Action**: Remove ToolRestrictionError references

**Steps**:
```bash
# Find all references in spec directory
grep -rn "ToolRestrictionError" specs/001-script-execution/

# Update each file to remove references
```

**Specific Updates**:
1. **tasks.md**: Remove T045-T047 tasks
2. **data-model.md**: Remove ToolRestrictionError class definition (line 367)
3. **IMPLEMENTATION_GUIDE.md**: Remove enforcement documentation (line 665)
4. **research-langchain-integration.md**: Remove ToolRestrictionError class (line 588)

#### 3.4 Update CLAUDE.md

**File**: `CLAUDE.md`

**Action**: Remove tool restriction references

**Steps**:
```bash
# Find references
grep -n "tool restriction\|ToolRestriction" CLAUDE.md

# Remove any references to enforcement feature
```

---

### Phase 4: Verification (30 minutes)

#### 4.1 Run test suite

**Command**:
```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest -v

# Check for any failures related to removed code
```

**Expected Result**:
- All tests pass
- No `ImportError` for `ToolRestrictionError`
- No `AttributeError` for `_check_tool_restrictions`

#### 4.2 Check test coverage

**Command**:
```bash
# Run with coverage
pytest --cov=src/skillkit --cov-report=term-missing

# Verify coverage remains ≥70%
```

**Expected Result**:
- Coverage: ≥70% (should remain stable or improve slightly)

#### 4.3 Lint and type check

**Command**:
```bash
# Lint code
ruff check src/skillkit

# Type check
mypy src/skillkit --strict
```

**Expected Result**:
- No linting errors
- No type errors

#### 4.4 Manual smoke test

**Script**: Create a test skill with `allowed-tools` that doesn't include "Bash"

**Steps**:
```bash
# Create test skill
mkdir -p /tmp/test-skill/scripts
cat > /tmp/test-skill/SKILL.md << 'EOF'
---
name: test-removal
description: Test script execution without Bash in allowed-tools
allowed-tools:
  - Read
  - Write
---

Test skill for verifying tool restriction removal.
EOF

cat > /tmp/test-skill/scripts/test.py << 'EOF'
import json
import sys
args = json.loads(sys.stdin.read())
print(json.dumps({"result": "success", "args": args}))
EOF

# Test script execution
python << 'EOF'
from pathlib import Path
from skillkit.core.models import SkillMetadata
from skillkit.core.scripts import ScriptExecutor

metadata = SkillMetadata(
    name="test-removal",
    description="Test",
    skill_path=Path("/tmp/test-skill/SKILL.md"),
    allowed_tools=("Read", "Write")  # No "Bash"
)

executor = ScriptExecutor(timeout=5)
result = executor.execute(
    Path("scripts/test.py"),
    {"test": "value"},
    Path("/tmp/test-skill"),
    metadata
)

print(f"Exit code: {result.exit_code}")
print(f"Stdout: {result.stdout}")
assert result.exit_code == 0, "Script should execute successfully"
print("✅ Test passed - script executed without tool restriction check")
EOF
```

**Expected Output**:
```
Exit code: 0
Stdout: {"result": "success", "args": {"test": "value"}}
✅ Test passed - script executed without tool restriction check
```

---

### Phase 5: Commit Changes (10 minutes)

#### 5.1 Review changes

**Command**:
```bash
# Check modified files
git status

# Review diffs
git diff src/skillkit/core/scripts.py
git diff src/skillkit/core/exceptions.py
git diff src/skillkit/integrations/langchain.py
```

#### 5.2 Commit code changes

**Command**:
```bash
# Stage code changes
git add src/skillkit/core/scripts.py
git add src/skillkit/core/exceptions.py
git add src/skillkit/integrations/langchain.py

# Commit with descriptive message
git commit -m "Remove tool restriction enforcement from script execution

- Remove ScriptExecutor._check_tool_restrictions() method
- Remove ToolRestrictionError exception class
- Keep allowed-tools field in SkillMetadata for backward compatibility
- No breaking changes to public API

Addresses spec clarification session 2025-11-30, Q2 and Q5"
```

#### 5.3 Commit test changes

**Command**:
```bash
# Stage test deletions
git add tests/test_script_executor_phase6.py
git add tests/test_script_executor.py
git add tests/fixtures/skills/restricted-skill/

# Commit test changes
git commit -m "Remove tool restriction tests

- Delete test_script_executor_phase6.py (T045-T047 tests)
- Remove ToolRestrictionError test cases from test_script_executor.py
- Delete restricted-skill test fixture

All other ScriptExecutor tests remain intact"
```

#### 5.4 Commit documentation changes

**Command**:
```bash
# Stage documentation updates
git add README.md
git add CLAUDE.md
git add examples/script_execution.py
git add specs/001-script-execution/*.md

# Commit documentation changes
git commit -m "Update documentation to remove tool restriction references

- Remove ToolRestrictionError from README examples
- Remove ToolRestrictionError from script_execution.py example
- Update spec documents to reflect removal
- Add Out of Scope section to spec.md clarifying non-enforcement

Backward compatible - allowed-tools field documentation preserved"
```

---

## Troubleshooting

### Issue 1: Tests fail with `ImportError`

**Error**:
```
ImportError: cannot import name 'ToolRestrictionError' from 'skillkit.core.exceptions'
```

**Solution**:
```bash
# Find all remaining imports
grep -rn "ToolRestrictionError" .

# Remove imports from identified files
```

### Issue 2: Tests fail with `AttributeError`

**Error**:
```
AttributeError: 'ScriptExecutor' object has no attribute '_check_tool_restrictions'
```

**Solution**:
```bash
# Find all method calls
grep -rn "_check_tool_restrictions" .

# Remove method calls from identified locations
```

### Issue 3: Coverage drops below 70%

**Cause**: Removal of tests reduces tested lines

**Solution**:
- Review uncovered lines with `pytest --cov-report=html`
- Coverage should remain stable (removing feature code + feature tests = no net change)
- If coverage drops, verify all non-restriction tests still run

### Issue 4: Mypy type errors

**Error**:
```
error: Name 'ToolRestrictionError' is not defined
```

**Solution**:
```bash
# Find all type annotations using ToolRestrictionError
grep -rn "ToolRestrictionError" src/

# Remove from type hints and docstrings
```

---

## Validation Checklist

Before considering the work complete, verify:

- [ ] `_check_tool_restrictions()` method removed from `scripts.py`
- [ ] Method call removed from `execute()` method (line 1134)
- [ ] `ToolRestrictionError` class removed from `exceptions.py`
- [ ] LangChain integration comment updated
- [ ] `test_script_executor_phase6.py` deleted
- [ ] ToolRestrictionError test case removed from `test_script_executor.py`
- [ ] `restricted-skill` fixture deleted
- [ ] README.md updated (no ToolRestrictionError references)
- [ ] examples/script_execution.py updated
- [ ] Spec documents updated (tasks.md, data-model.md, etc.)
- [ ] CLAUDE.md updated
- [ ] All tests pass (`pytest -v`)
- [ ] Test coverage ≥70% (`pytest --cov`)
- [ ] No linting errors (`ruff check`)
- [ ] No type errors (`mypy --strict`)
- [ ] Manual smoke test passes
- [ ] Git commits created with clear messages

---

## Expected Outcome

After completing this quickstart:

1. **Code Simplified**: ~250 lines of code removed
2. **Backward Compatible**: `allowed-tools` field remains, no API breaking changes
3. **Tests Updated**: Restriction tests removed, other tests still pass
4. **Documentation Current**: All references to enforcement removed
5. **Feature Removed**: Scripts execute regardless of `allowed-tools` value

---

## Next Steps

1. Run final verification (`pytest`, `ruff`, `mypy`)
2. Push changes to remote branch
3. Create pull request with summary of changes
4. Request code review
5. Merge after approval
6. Update changelog for v0.3.x release

---

## Estimated Time Breakdown

| Phase | Task | Estimated Time |
|-------|------|----------------|
| 1 | Code Removal | 30 minutes |
| 2 | Test Removal | 20 minutes |
| 3 | Documentation Updates | 40 minutes |
| 4 | Verification | 30 minutes |
| 5 | Commit Changes | 10 minutes |
| **Total** | | **2 hours 10 minutes** |

Plus buffer for troubleshooting: **2-3 hours total**
