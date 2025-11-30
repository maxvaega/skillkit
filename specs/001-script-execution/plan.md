# Implementation Plan: Remove Tool Restriction Enforcement

**Branch**: `001-script-execution` | **Date**: 2025-11-30 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-script-execution/spec.md`

**Note**: This plan removes the tool restriction enforcement feature (FR-008 and related code) while preserving the `allowed-tools` field in SkillMetadata for backward compatibility.

## Summary

Remove all tool restriction enforcement code for script execution while maintaining backward compatibility with the `allowed-tools` field in SkillMetadata. This includes:
- Removing the `_check_tool_restrictions()` method from ScriptExecutor (src/skillkit/core/scripts.py:833-869)
- Removing ToolRestrictionError exception class from exceptions.py (src/skillkit/core/exceptions.py:427-461)
- Removing all test files and test cases related to tool restrictions
- Removing references from documentation, examples, and specs
- Keeping the `allowed-tools` field in SkillMetadata for backward compatibility (no enforcement)

## Technical Context

**Language/Version**: Python 3.10+ (minimum for existing skillkit v0.3.0 compatibility)
**Primary Dependencies**: PyYAML 6.0+ (existing), aiofiles 23.0+ (existing), subprocess (stdlib), pathlib (stdlib)
**Storage**: Filesystem-based (Python source files and test files to be modified/removed)
**Testing**: pytest 7.0+ with parametrized tests for regression coverage
**Target Platform**: Cross-platform (Linux, macOS, Windows) - same as existing skillkit
**Project Type**: Single Python library (src/skillkit/ with tests/)
**Performance Goals**: No performance impact - code removal only (potential minor improvement from eliminating security check)
**Constraints**: Backward compatibility - must preserve `allowed-tools` field in SkillMetadata, all existing APIs must remain functional
**Scale/Scope**: Affects 8 source files, 15+ test files, 10+ documentation files - clean removal without breaking changes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Status: ✅ PASS

**Principle: Backward Compatibility**
- Status: ✅ PASS
- Rationale: The `allowed-tools` field remains in SkillMetadata for backward compatibility. Existing code that reads this field will continue to work. No breaking API changes.

**Principle: Simplicity (YAGNI)**
- Status: ✅ PASS
- Rationale: Removing unused enforcement code aligns with YAGNI. The spec clarifies this feature is intentionally not enforced ("Out of Scope" section).

**Principle: Test Coverage**
- Status: ✅ PASS
- Rationale: Removal of test files is intentional (testing removed functionality). Regression tests will verify existing script execution still works.

**Principle: Security**
- Status: ✅ PASS
- Rationale: Tool restriction enforcement was never a security boundary (spec assumption: "Scripts are provided by trusted skill authors"). Other security controls (path validation, permission checks, timeout) remain intact.

**No Constitution Violations**: This change simplifies the codebase by removing an unused feature without introducing complexity or breaking changes.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/skillkit/
├── core/
│   ├── scripts.py                 # MODIFY: Remove _check_tool_restrictions() method (lines 833-869)
│   │                              #         Remove call to _check_tool_restrictions() in execute() (line 1134)
│   ├── exceptions.py              # MODIFY: Remove ToolRestrictionError class (lines 427-461)
│   ├── models.py                  # NO CHANGE: Keep allowed_tools field in SkillMetadata for backward compatibility
│   └── manager.py                 # NO CHANGE: No tool restriction logic here
├── integrations/
│   └── langchain.py               # MODIFY: Remove ToolRestrictionError from imports and exception handling (line 330)

tests/
├── test_script_executor.py        # MODIFY: Remove ToolRestrictionError test cases (line 420 and related)
├── test_script_executor_phase6.py # DELETE: Entire file (150+ lines testing tool restrictions)
├── test_script_executor_phase3.py # REVIEW: Check for ToolRestrictionError references
├── test_script_executor_phase4.py # REVIEW: Check for ToolRestrictionError references
├── test_models.py                 # NO CHANGE: allowed_tools field tests remain (backward compatibility)
├── test_parser.py                 # NO CHANGE: allowed_tools parsing tests remain (backward compatibility)
└── fixtures/skills/
    └── restricted-skill/          # DELETE: Entire skill directory (test fixture for tool restrictions)

examples/
├── script_execution.py            # MODIFY: Remove ToolRestrictionError from imports and exception handling (line 26)
└── basic_usage.py                 # NO CHANGE: No tool restriction references

Documentation Files:
├── README.md                      # MODIFY: Remove ToolRestrictionError from examples (lines 442, 456)
├── CLAUDE.md                      # MODIFY: Remove tool restriction references
└── specs/001-script-execution/
    ├── spec.md                    # MODIFY: Already updated - FR-008 removed, Out of Scope section added
    ├── tasks.md                   # MODIFY: Remove T045-T047, remove tool restriction user story
    ├── data-model.md              # MODIFY: Remove ToolRestrictionError references (line 367)
    ├── IMPLEMENTATION_GUIDE.md    # MODIFY: Remove ToolRestrictionError references (line 665)
    ├── research-langchain-integration.md  # MODIFY: Remove ToolRestrictionError class definition (line 588)
    └── CROSS_PLATFORM_INDEX.md    # REVIEW: Check for tool restriction references
```

**Structure Decision**: Single Python library project. All changes are code removals or documentation updates. No new files created. The core modification is removing enforcement logic while preserving the `allowed-tools` field for backward compatibility.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - No constitution violations. This change reduces complexity by removing code.

---

## Phase 0: Research & Planning ✅ COMPLETE

**Objective**: Understand scope of removal and identify all affected code

**Outputs**:
- ✅ `research-removal-tool-restrictions.md` - Analysis of what needs to be removed
- ✅ `plan.md` (this file) - Implementation roadmap

**Key Findings**:
1. **Code Removal**: 2 methods (~70 lines total)
   - `ScriptExecutor._check_tool_restrictions()` (37 lines)
   - `ToolRestrictionError` exception class (35 lines)

2. **Test Removal**: 3 test artifacts (~200 lines total)
   - `test_script_executor_phase6.py` (entire file, 150+ lines)
   - Test case in `test_script_executor.py` (line 420)
   - Test fixture `tests/fixtures/skills/restricted-skill/` (directory)

3. **Documentation Updates**: 10+ files
   - README.md, CLAUDE.md, examples/script_execution.py
   - 6 spec documents in `specs/001-script-execution/`

4. **Backward Compatibility Strategy**:
   - ✅ Keep `allowed-tools` field in SkillMetadata
   - ✅ Keep YAML parsing for `allowed-tools`
   - ✅ Keep field tests (test_parser.py, test_models.py)
   - ❌ Remove only enforcement logic

**Risks Identified**:
- Low risk: Code importing `ToolRestrictionError` will break (need to update)
- Low risk: Test dependencies on deleted fixtures (run pytest to find)
- Medium risk: Documentation inconsistency (systematic review needed)

**Mitigation**:
- Comprehensive grep for all references before removal
- Run pytest after each deletion to catch dependencies
- Systematic documentation review with keyword search

---

## Phase 1: Design & Contracts ✅ COMPLETE

**Objective**: Document the changes to data models and APIs

**Outputs**:
- ✅ `data-model-removal-tool-restrictions.md` - Changes to data models
- ✅ `contracts/removal-api-contract.md` - API changes and backward compatibility guarantees
- ✅ `quickstart-removal-tool-restrictions.md` - Step-by-step implementation guide

**Key Decisions**:
1. **SkillMetadata**: No changes (field preserved for backward compatibility)
2. **ScriptExecutor**: Remove `_check_tool_restrictions()` method entirely
3. **ToolRestrictionError**: Delete exception class completely
4. **Tests**: Delete restriction-specific tests, keep field parsing tests
5. **Documentation**: Remove all references to enforcement

**Contracts Defined**:
- **Public API**: No breaking changes (except exception class removal)
- **Behavioral Change**: Scripts execute regardless of `allowed-tools` value
- **Backward Compatibility**: 100% for field access, breaking for exception handling
- **Migration Path**: Remove imports and exception handlers

**Agent Context Updated**: ✅
- Technology stack documented in CLAUDE.md
- Active technologies list updated with removal context

---

## Phase 2: Implementation Planning (Next Step: /speckit.tasks)

**Objective**: Generate actionable tasks for implementation

**Status**: ⏳ PENDING - Run `/speckit.tasks` to generate tasks.md

**Expected Tasks**:
1. Code removal tasks (5-7 tasks)
   - Remove `_check_tool_restrictions()` method
   - Remove method call from `execute()`
   - Remove `ToolRestrictionError` class
   - Update LangChain integration comment

2. Test removal tasks (3-5 tasks)
   - Delete `test_script_executor_phase6.py`
   - Remove test case from `test_script_executor.py`
   - Delete `restricted-skill` fixture
   - Add regression test for backward compatibility

3. Documentation tasks (10+ tasks)
   - Update README.md (2 locations)
   - Update examples/script_execution.py
   - Update 6 spec documents
   - Update CLAUDE.md

4. Verification tasks (4-6 tasks)
   - Run pytest suite
   - Check coverage ≥70%
   - Run linting (ruff)
   - Run type checking (mypy)
   - Manual smoke test
   - Commit changes

**Note**: This phase will be completed by running the `/speckit.tasks` command, which will generate a detailed task breakdown in `tasks.md`.

---

## Summary & Next Steps

**Current Status**: ✅ Planning Complete - Ready for Task Generation

**Completed**:
1. ✅ Analyzed existing implementation (Phase 0)
2. ✅ Identified all code to be removed (Phase 0)
3. ✅ Researched security and compatibility implications (Phase 0)
4. ✅ Designed data model changes (Phase 1)
5. ✅ Defined API contracts (Phase 1)
6. ✅ Created quickstart implementation guide (Phase 1)
7. ✅ Updated agent context (Phase 1)

**Next Action**: Run `/speckit.tasks` to generate implementation tasks

**Estimated Implementation Time**: 2-3 hours (per quickstart guide)

**Files Generated**:
- `specs/001-script-execution/plan.md` (this file)
- `specs/001-script-execution/research-removal-tool-restrictions.md`
- `specs/001-script-execution/data-model-removal-tool-restrictions.md`
- `specs/001-script-execution/contracts/removal-api-contract.md`
- `specs/001-script-execution/quickstart-removal-tool-restrictions.md`

**Branch**: `001-script-execution`
**Ready for**: Task generation and implementation
