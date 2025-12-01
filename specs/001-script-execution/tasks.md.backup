# Tasks: Remove Tool Restriction Enforcement

**Input**: Design documents from `/specs/001-script-execution/`
**Prerequisites**: plan.md, spec.md (updated with FR-008 removed), research-removal-tool-restrictions.md, data-model-removal-tool-restrictions.md, contracts/removal-api-contract.md, quickstart-removal-tool-restrictions.md

**Feature**: Remove all tool restriction enforcement code while preserving `allowed-tools` field for backward compatibility

**Organization**: Tasks organized by functional area (code removal, test removal, documentation updates, verification)

**Context**: This feature removes previously implemented tool restriction enforcement (FR-008, User Story 4) while maintaining backward compatibility with the `allowed-tools` field in SkillMetadata.

## Format: `- [ ] [ID] [P?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- File paths are absolute from repository root

---

## Phase 1: Pre-Removal Analysis

**Purpose**: Identify all references to tool restrictions before removal

- [ ] T001 Search for all occurrences of `ToolRestrictionError` in codebase using grep: `grep -r "ToolRestrictionError" src/ tests/ examples/`
- [ ] T002 Search for all occurrences of `_check_tool_restrictions` in codebase using grep: `grep -r "_check_tool_restrictions" src/ tests/`
- [ ] T003 Search for all occurrences of "tool restriction" in documentation files using grep: `grep -r "tool restriction" README.md CLAUDE.md .docs/ specs/`
- [ ] T004 Search for all test files containing tool restriction tests using grep: `grep -r "test.*tool.*restriction" tests/`
- [ ] T005 Create backup of current branch state: `git stash` or `git branch backup-before-removal`

**Checkpoint**: All references identified (expect ~8 source file references, ~15 test file references, ~10 doc references) - ready for systematic removal

---

## Phase 2: Core Code Removal

**Purpose**: Remove enforcement logic from source code

### Exception Class Removal

- [ ] T006 Remove `ToolRestrictionError` exception class definition from src/skillkit/core/exceptions.py (lines 427-461 per plan.md)
- [ ] T007 Remove `ToolRestrictionError` from `__all__` export list in src/skillkit/core/exceptions.py if present

### ScriptExecutor Method Removal

- [ ] T008 Remove `_check_tool_restrictions()` private method from src/skillkit/core/scripts.py (lines 833-869 per plan.md)
- [ ] T009 Remove call to `self._check_tool_restrictions()` in `execute()` method in src/skillkit/core/scripts.py (line 1134 per plan.md)
- [ ] T010 Update docstring for `execute()` method to remove `ToolRestrictionError` from "Raises" section in src/skillkit/core/scripts.py

### Integration Updates

- [ ] T011 [P] Remove `ToolRestrictionError` from import statement in src/skillkit/integrations/langchain.py
- [ ] T012 [P] Remove or update comment mentioning `ToolRestrictionError` in exception handling in src/skillkit/integrations/langchain.py (line 330 per plan.md)
- [ ] T013 [P] Remove `ToolRestrictionError` from exports in src/skillkit/__init__.py if present

### Model Verification (NO CHANGES)

- [ ] T014 Verify `allowed_tools` field remains in SkillMetadata in src/skillkit/core/models.py (should see NO changes to this file)
- [ ] T015 Verify parser.py still parses `allowed-tools` from YAML (should see NO changes to src/skillkit/core/parser.py)

**Checkpoint**: Core enforcement code removed - scripts now execute without tool restriction checks (verify with `grep -r "ToolRestrictionError" src/`)

---

## Phase 3: Test Removal

**Purpose**: Remove tests related to tool restriction enforcement while preserving field parsing tests

### Test File Deletion

- [ ] T016 Delete entire test file tests/test_script_executor_phase6.py (150+ lines testing tool restrictions per plan.md)
- [ ] T017 Delete test fixture directory tests/fixtures/skills/restricted-skill/ (tool restriction test fixture per plan.md)

### Test Case Removal from Existing Files

- [ ] T018 Remove `ToolRestrictionError` test case from tests/test_script_executor.py (around line 420 per plan.md)
- [ ] T019 [P] Search and remove any `ToolRestrictionError` references from tests/test_script_executor_phase3.py
- [ ] T020 [P] Search and remove any `ToolRestrictionError` references from tests/test_script_executor_phase4.py
- [ ] T021 [P] Search and remove any `ToolRestrictionError` import statements from all test files

### Backward Compatibility Tests (KEEP THESE - NO CHANGES)

- [ ] T022 Verify tests for `allowed_tools` field parsing in tests/test_parser.py remain unchanged (grep should find no changes)
- [ ] T023 Verify tests for `allowed_tools` field in SkillMetadata in tests/test_models.py remain unchanged (grep should find no changes)

**Checkpoint**: Tool restriction tests removed - test suite should pass with ~200 fewer lines of test code (verify with `pytest -v`)

---

## Phase 4: Documentation Updates

**Purpose**: Remove all references to tool restriction enforcement from documentation

### Main Documentation Files

- [ ] T024 [P] Remove `ToolRestrictionError` example from README.md (lines 442, 456 per plan.md)
- [ ] T025 [P] Remove "Tool restriction enforcement" from v0.3.0 feature list in CLAUDE.md
- [ ] T026 [P] Update CLAUDE.md "Active Technologies" section to remove tool restriction references
- [ ] T027 [P] Remove `ToolRestrictionError` import from examples/script_execution.py (line 26 per plan.md)
- [ ] T028 [P] Remove `ToolRestrictionError` exception handler from examples/script_execution.py if present

### Spec Documents in specs/001-script-execution/

- [ ] T029 [P] Remove `ToolRestrictionError` reference from specs/001-script-execution/data-model.md (line 367 per plan.md)
- [ ] T030 [P] Remove `ToolRestrictionError` reference from specs/001-script-execution/IMPLEMENTATION_GUIDE.md (line 665 per plan.md)
- [ ] T031 [P] Remove `ToolRestrictionError` class definition from specs/001-script-execution/research-langchain-integration.md (line 588 per plan.md)
- [ ] T032 [P] Search and remove tool restriction references from specs/001-script-execution/CROSS_PLATFORM_INDEX.md if any exist

### Spec Document Verification

- [ ] T033 Verify specs/001-script-execution/spec.md correctly shows FR-008 removed and "Out of Scope" section updated
- [ ] T034 Verify specs/001-script-execution/plan.md reflects removal strategy (current plan.md is correct)
- [ ] T035 Verify specs/001-script-execution/contracts/removal-api-contract.md documents the API changes correctly

**Checkpoint**: Documentation cleaned - all references to enforcement removed (verify with `grep -ri "ToolRestrictionError" README.md CLAUDE.md examples/ specs/`)

---

## Phase 5: Regression Testing & Verification

**Purpose**: Ensure removal didn't break existing functionality

### Test Execution

- [ ] T036 Run full pytest suite to verify all tests pass: `pytest -v`
- [ ] T037 Run pytest with coverage to verify ≥70% coverage maintained: `pytest --cov=src/skillkit --cov-report=term-missing`
- [ ] T038 [P] Run async tests specifically: `pytest -m async -v`
- [ ] T039 [P] Run integration tests specifically: `pytest -m integration -v`

### Code Quality Checks

- [ ] T040 [P] Run ruff linting to verify no new issues: `ruff check src/skillkit`
- [ ] T041 [P] Run ruff formatting check: `ruff format --check src/skillkit`
- [ ] T042 [P] Run mypy type checking in strict mode: `mypy src/skillkit --strict`

### Functional Validation

- [ ] T043 [P] Run examples/basic_usage.py to verify core functionality: `python examples/basic_usage.py`
- [ ] T044 [P] Run examples/script_execution.py to verify script execution: `python examples/script_execution.py`
- [ ] T045 [P] Run examples/async_usage.py to verify async functionality: `python examples/async_usage.py`
- [ ] T046 Manual test: Create skill with `allowed-tools: [Read, Write]` (no Bash) and verify script executes successfully without ToolRestrictionError

**Checkpoint**: All tests pass (pytest should report fewer tests due to phase6 deletion), code quality verified, functionality intact

---

## Phase 6: Backward Compatibility Verification

**Purpose**: Ensure existing APIs continue to work (except for expected breaking change)

### API Compatibility Tests

- [ ] T047 Verify `SkillMetadata.allowed_tools` field is still accessible: `python -c "from skillkit.core.models import SkillMetadata; print(hasattr(SkillMetadata, 'allowed_tools'))"`
- [ ] T048 Verify `ScriptExecutor.execute()` method signature unchanged (check docstring, parameters)
- [ ] T049 Verify YAML parsing of `allowed-tools` field continues to work (check test_parser.py tests pass)
- [ ] T050 Verify LangChain tool creation works for skills with and without `allowed-tools` field

### Security Features Verification (MUST STILL WORK)

- [ ] T051 [P] Verify PathSecurityError still works: `python -c "from skillkit.core.exceptions import PathSecurityError"`
- [ ] T052 [P] Verify ScriptPermissionError still works: `python -c "from skillkit.core.exceptions import ScriptPermissionError"`
- [ ] T053 [P] Verify InterpreterNotFoundError still works: `python -c "from skillkit.core.exceptions import InterpreterNotFoundError"`
- [ ] T054 Verify path traversal prevention still blocks ../../etc/passwd attacks
- [ ] T055 Verify setuid/setgid permission checks still reject dangerous scripts

### Breaking Change Verification (EXPECTED)

- [ ] T056 Verify `ToolRestrictionError` import fails with ImportError: `python -c "from skillkit.core.exceptions import ToolRestrictionError"` (should fail)
- [ ] T057 Document that this is the ONLY expected breaking change

**Checkpoint**: Backward compatibility verified except for documented `ToolRestrictionError` removal

---

## Phase 7: Final Polish & Commit

**Purpose**: Clean up and prepare for PR/merge

### Final Cleanup

- [ ] T058 [P] Search entire codebase for any missed "tool restriction" references: `grep -ri "tool.restriction" src/ tests/ examples/ README.md CLAUDE.md`
- [ ] T059 [P] Search for any remaining `ToolRestrictionError` references: `grep -r "ToolRestrictionError" src/ tests/ examples/`
- [ ] T060 [P] Search for any remaining `_check_tool_restrictions` references: `grep -r "_check_tool_restrictions" src/ tests/`
- [ ] T061 Review git diff to ensure only intended changes are included: `git diff --stat` and `git diff`

### Version & Changelog

- [ ] T062 Verify version in pyproject.toml remains 0.3.0 (this is a patch within 0.3.x, not a major bump)
- [ ] T063 Verify version in src/skillkit/__init__.py remains 0.3.0
- [ ] T064 Add changelog entry to README.md under v0.3.0 section: "Removed tool restriction enforcement while preserving allowed-tools field for backward compatibility"
- [ ] T065 Update CLAUDE.md v0.3.0 description to clarify tool restriction enforcement removed

### Git Operations

- [ ] T066 Review all staged changes: `git status` and `git diff --cached`
- [ ] T067 Create commit with descriptive message: `git commit -m "Remove tool restriction enforcement

Remove ToolRestrictionError exception class and _check_tool_restrictions() method
while preserving allowed-tools field in SkillMetadata for backward compatibility.

- Remove src/skillkit/core/exceptions.py ToolRestrictionError class (lines 427-461)
- Remove src/skillkit/core/scripts.py _check_tool_restrictions() method (lines 833-869)
- Remove tests/test_script_executor_phase6.py (tool restriction tests)
- Remove tests/fixtures/skills/restricted-skill/ test fixture
- Update documentation to remove enforcement references
- Scripts now execute regardless of allowed-tools value

Breaking change: ToolRestrictionError import will fail (documented in contracts/)
All other APIs remain backward compatible.

Refs: specs/001-script-execution/plan.md, contracts/removal-api-contract.md"`
- [ ] T068 Verify commit includes all intended changes: `git show --stat`
- [ ] T069 Push to branch 001-script-execution: `git push origin 001-script-execution`

**Checkpoint**: All changes committed and pushed - ready for PR or merge

---

## Dependencies & Execution Order

### Phase Dependencies

1. **Pre-Removal Analysis (Phase 1)**: No dependencies - can start immediately ✅
2. **Core Code Removal (Phase 2)**: Depends on Phase 1 (need to know what to remove) ⏳
3. **Test Removal (Phase 3)**: Depends on Phase 2 (tests reference removed code) ⏳
4. **Documentation Updates (Phase 4)**: Can run in parallel with Phase 3 after Phase 2 complete 🔀
5. **Regression Testing (Phase 5)**: Depends on Phases 2, 3, 4 completion (all changes done) ⏳
6. **Backward Compatibility (Phase 6)**: Depends on Phase 5 (tests must pass first) ⏳
7. **Final Polish (Phase 7)**: Depends on Phase 6 (final verification) ⏳

### Within Each Phase

**Phase 2 (Core Code Removal)**:
- T006-T007: Exception removal (sequential, same file)
- T008-T010: ScriptExecutor updates (sequential, same file)
- T011-T013: Integration updates (can parallelize [P], different files)
- T014-T015: Verification only (can parallelize [P])

**Phase 3 (Test Removal)**:
- T016-T017: File/directory deletion (can parallelize)
- T018-T021: Test case removal (can parallelize [P], different files)
- T022-T023: Verification only (can parallelize [P])

**Phase 4 (Documentation)**:
- T024-T028: Main docs (can parallelize [P], all different files)
- T029-T032: Spec docs (can parallelize [P], all different files)
- T033-T035: Verification only (sequential reading)

**Phase 5 (Testing)**:
- T036-T037: pytest runs (sequential, observe results)
- T038-T039: Specific test markers (can parallelize [P])
- T040-T042: Code quality (can parallelize [P], different tools)
- T043-T046: Functional tests (can parallelize [P], different scripts)

**Phase 6 (Compatibility)**:
- T047-T050: API tests (can parallelize)
- T051-T055: Security tests (can parallelize [P])
- T056-T057: Breaking change verification (sequential)

**Phase 7 (Polish)**:
- T058-T061: Final searches (can parallelize [P])
- T062-T065: Version/changelog (sequential, related)
- T066-T069: Git operations (MUST be sequential)

### Parallel Opportunities

```bash
# Phase 2: Integration updates in parallel
Task T011: Remove from langchain.py
Task T012: Update langchain.py comments
Task T013: Remove from __init__.py

# Phase 3: Test file cleanup in parallel
Task T016: Delete test_script_executor_phase6.py
Task T017: Delete tests/fixtures/skills/restricted-skill/
Task T019: Clean test_script_executor_phase3.py
Task T020: Clean test_script_executor_phase4.py

# Phase 4: All documentation updates in parallel (8 tasks)
Task T024-T032: Update all doc files concurrently

# Phase 5: Code quality checks in parallel
Task T040: ruff check
Task T041: ruff format
Task T042: mypy

Task T043-T046: Run all example scripts concurrently

# Phase 6: Security verification in parallel
Task T051-T055: Verify all security features work

# Phase 7: Final searches in parallel
Task T058-T060: Run all grep searches concurrently
```

---

## Implementation Strategy

### Recommended Approach: Sequential by Phase

This is a **code removal** task, not a feature implementation. The safest approach:

1. **Phase 1** (30 min): Identify all references with grep searches
2. **Phase 2** (1 hour): Remove core code systematically
3. **Phase 3** (30 min): Delete test files and test cases
4. **Phase 4** (1-1.5 hours): Update documentation (can parallelize tasks)
5. **Phase 5** (1 hour): Run comprehensive tests and validation
6. **Phase 6** (30 min): Verify backward compatibility
7. **Phase 7** (30 min): Final cleanup, review, commit, push

**Total estimated time**: ~5-6 hours for thorough work, ~2-3 hours for experienced developers (per quickstart.md)

### Critical Path Tasks

These tasks MUST complete successfully (blocking):

1. **T008**: Remove `_check_tool_restrictions()` method (core change)
2. **T009**: Remove method call in `execute()` (prevents runtime errors)
3. **T016**: Delete phase6 test file (removes failing tests)
4. **T036**: pytest passes (verification gate) ← CRITICAL CHECKPOINT
5. **T046**: Manual functional test (verify scripts execute without restriction)

**If any critical path task fails, STOP and debug before proceeding.**

### Optimization: Parallel Documentation Updates

Phase 4 has 12 tasks that can run in parallel:
- Assign 3 tasks per developer for 4x speedup
- Or use parallel grep + sed for bulk updates

---

## Success Criteria

### Functional Success ✅

- [ ] All tests pass: `pytest -v` returns exit code 0
- [ ] Coverage ≥70% maintained: `pytest --cov` shows coverage
- [ ] Scripts execute regardless of `allowed-tools` value (manual test T046 passes)
- [ ] No `ToolRestrictionError` references in src/, tests/, examples/: `grep -r "ToolRestrictionError" src/ tests/ examples/` returns empty

### API Success ✅

- [ ] `SkillMetadata.allowed_tools` field still accessible (T047 passes)
- [ ] `ScriptExecutor.execute()` signature unchanged (T048 passes)
- [ ] YAML parsing continues to work (T049 passes)
- [ ] LangChain integration works (T050 passes)
- [ ] All security features intact: PathSecurityError, ScriptPermissionError, etc. (T051-T055 pass)

### Documentation Success ✅

- [ ] README.md updated (no ToolRestrictionError references)
- [ ] CLAUDE.md updated (v0.3.0 description reflects removal)
- [ ] examples/script_execution.py updated (no ToolRestrictionError import)
- [ ] All spec docs updated (data-model.md, IMPLEMENTATION_GUIDE.md, etc.)

### Code Quality Success ✅

- [ ] ruff linting passes: `ruff check src/skillkit` (T040)
- [ ] ruff formatting passes: `ruff format --check src/skillkit` (T041)
- [ ] mypy type checking passes: `mypy src/skillkit --strict` (T042)
- [ ] No new warnings introduced

### Breaking Change Documented ✅

- [ ] `ToolRestrictionError` import fails as expected (T056)
- [ ] Breaking change documented in contracts/removal-api-contract.md (T057)
- [ ] Changelog updated (T064-T065)

---

## Risk Mitigation

### Risk 1: Accidentally removing security features

**Severity**: HIGH 🔴
**Probability**: LOW (clear identification in plan.md)

**Mitigation**:
- T014-T015: Verify models.py and parser.py unchanged
- T054-T055: Verify path validation and permission checks still work
- T051-T053: Verify all other exceptions work
- Phase 6 comprehensive security testing

**Detection**: T046 manual test, T054-T055 security verification

---

### Risk 2: Breaking backward compatibility unintentionally

**Severity**: HIGH 🔴
**Probability**: LOW (only removing enforcement, not field)

**Mitigation**:
- T014: Verify `allowed_tools` field preserved in SkillMetadata
- T022-T023: Verify field parsing tests unchanged
- T047-T050: Comprehensive API compatibility tests
- Phase 6 dedicated to compatibility verification

**Detection**: T036-T037 pytest runs, Phase 6 tests

---

### Risk 3: Missing documentation references

**Severity**: MEDIUM 🟡
**Probability**: MEDIUM (many files to update)

**Mitigation**:
- T001-T004: Comprehensive grep searches before removal
- T058-T060: Final verification searches after removal
- T061: Git diff review
- Phase 4 systematic documentation updates

**Detection**: T058-T060 grep searches should return empty

---

### Risk 4: Test suite fails after removal

**Severity**: HIGH 🔴
**Probability**: LOW (test files clearly identified)

**Mitigation**:
- T016-T017: Delete entire phase6 test file (clean removal)
- T018-T021: Remove specific test cases referencing ToolRestrictionError
- T036-T039: Comprehensive pytest execution
- Stop at Phase 5 checkpoint if any test fails

**Detection**: T036 pytest run (critical checkpoint)

---

### Risk 5: Git merge conflicts

**Severity**: LOW 🟢
**Probability**: LOW (working on feature branch)

**Mitigation**:
- T005: Create backup before changes
- T066-T068: Careful review of staged changes
- Feature branch 001-script-execution isolated from main

**Detection**: T066 git status review

---

## Notes

- This is a **code removal** feature, not a typical implementation - most tasks involve deleting code
- The `allowed-tools` field is **preserved** for backward compatibility - NO changes to SkillMetadata or parser
- **Only breaking change**: `ToolRestrictionError` import will fail - this is documented and expected
- **Behavioral change**: Scripts execute without tool restriction checks - this is the goal
- All security features (path validation, permission checks, timeout, output limits) remain fully intact
- Test count will decrease by ~150 lines (phase6 file removal)
- Estimated total time: 2-3 hours (experienced), 5-6 hours (thorough)

---

## Quickstart Integration

This tasks.md integrates with quickstart-removal-tool-restrictions.md:

**Quickstart provides**:
- Step-by-step implementation guide
- Code examples for removal
- Expected outcomes at each step

**This tasks.md provides**:
- Granular task breakdown (69 tasks)
- Exact file paths and line numbers
- Parallel execution opportunities
- Success criteria and verification

**Usage**:
1. Read quickstart.md for overview and approach
2. Follow this tasks.md for detailed execution
3. Reference plan.md for strategic context
4. Check contracts/removal-api-contract.md for API impact

---

## Post-Implementation Checklist

After completing all tasks, verify:

- [ ] `grep -r "ToolRestrictionError" src/ tests/ examples/` returns zero results
- [ ] `grep -r "_check_tool_restrictions" src/ tests/` returns zero results
- [ ] `pytest -v` passes with no failures
- [ ] `pytest --cov` shows ≥70% coverage
- [ ] `ruff check src/skillkit` passes
- [ ] `mypy src/skillkit --strict` passes
- [ ] Manual test: Script executes with `allowed-tools: [Read]` (no Bash)
- [ ] Git diff reviewed and commit message is clear
- [ ] All documentation updated
- [ ] Breaking change documented

**Ready for**: PR creation or direct merge to main
