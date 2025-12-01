# Tasks: Tool ID Format Update for Script Execution

**Input**: Design documents from `/specs/001-script-execution/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and verification of test environment

- [ ] T001 Verify Python 3.10+ environment is active and all dependencies are installed
- [ ] T002 Create backup of current branch state before making changes
- [ ] T003 [P] Run existing test suite to establish baseline (pytest -v)

---

## Phase 2: Foundational (Core Changes - Blocking)

**Purpose**: Core tool ID format and validation changes that MUST be complete before any other work

**⚠️ CRITICAL**: No user story work or test updates can begin until this phase is complete

- [ ] T004 Add ToolIDValidationError exception class to src/skillkit/core/exceptions.py
- [ ] T005 Export ToolIDValidationError in src/skillkit/__init__.py
- [ ] T006 Add validate_tool_id() function to src/skillkit/core/scripts.py
- [ ] T007 Update ScriptMetadata.get_fully_qualified_name() method in src/skillkit/core/scripts.py to use new format
- [ ] T008 Update tool name generation in src/skillkit/integrations/langchain.py to use new format
- [ ] T009 Run quick validation test to ensure new format and validation work correctly

**Checkpoint**: Core implementation ready - test updates and documentation can now proceed in parallel

---

## Phase 3: User Story 1 - Update Core Implementation and Validation (Priority: P1) 🎯 MVP

**Goal**: Update the tool ID format from `skill-name.tool_name` to `skill-name__tool_name` with validation to ensure LLM provider compatibility

**Independent Test**: Can be verified by creating a test skill with scripts, generating tool IDs, and confirming they match the regex pattern `^[a-z0-9-]+__[a-z0-9_]+$` with max 60 characters

### Implementation for User Story 1

- [ ] T010 [P] [US1] Update test_scripts.py assertions to expect new tool ID format (skill-name__script-name)
- [ ] T011 [P] [US1] Update test_langchain.py assertions to expect new tool ID format
- [ ] T012 [P] [US1] Update test_script_langchain_integration.py assertions to expect new tool ID format
- [ ] T013 [P] [US1] Add unit tests for validate_tool_id() function in test_scripts.py (valid formats, invalid formats, length limits)
- [ ] T014 [P] [US1] Add unit tests for ToolIDValidationError exception in test_exceptions.py
- [ ] T015 [US1] Update any other test files that reference the old format (grep for patterns like skill_name.script_name)
- [ ] T016 [US1] Run full test suite and fix any remaining test failures (pytest -v)
- [ ] T017 [US1] Verify test coverage remains at 70%+ (pytest --cov)

**Checkpoint**: At this point, all core implementation and tests should pass with the new format

---

## Phase 4: User Story 2 - Update Documentation and Examples (Priority: P2)

**Goal**: Update all documentation and examples to reflect the new tool ID format and validation requirements

**Independent Test**: Can be verified by reviewing README.md and examples to ensure all tool ID references use the new format and explain validation rules

### Implementation for User Story 2

- [ ] T018 [P] [US2] Update README.md script execution section with new tool ID format and validation requirements
- [ ] T019 [P] [US2] Create or update examples/script_execution.py with examples using new tool ID format
- [ ] T020 [P] [US2] Update docstrings in src/skillkit/core/scripts.py to document new format
- [ ] T021 [P] [US2] Update docstrings in src/skillkit/integrations/langchain.py to document new format
- [ ] T022 [US2] Search codebase for any remaining references to old format in comments or documentation
- [ ] T023 [US2] Verify all example code runs correctly with new format

**Checkpoint**: All documentation and examples should reflect the new tool ID format

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [ ] T024 [P] Run full test suite one final time (pytest -v)
- [ ] T025 [P] Run type checking (mypy src/skillkit --strict)
- [ ] T026 [P] Run linting (ruff check src/skillkit)
- [ ] T027 [P] Run formatting check (ruff format --check src/skillkit)
- [ ] T028 Review all changes for security implications
- [ ] T029 Update CLAUDE.md with v0.3.0 release notes if needed
- [ ] T030 Verify backward compatibility notes are accurate (no existing deployments affected)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: Both depend on Foundational phase completion
  - User Story 1 and 2 can proceed in parallel once Foundational is complete
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of User Story 1

### Within Each User Story

- Phase 2 changes must complete before any test updates (T004-T009 before T010-T017)
- Test updates can run in parallel within User Story 1 (T010-T014 all marked [P])
- Documentation updates can run in parallel within User Story 2 (T018-T021 all marked [P])

### Parallel Opportunities

- All Setup tasks (T001-T003) can run in parallel
- All test update tasks in User Story 1 (T010-T014) can run in parallel after Phase 2
- All documentation tasks in User Story 2 (T018-T021) can run in parallel after Phase 2
- User Story 1 and User Story 2 can be worked on in parallel after Phase 2
- All Polish tasks (T024-T027) can run in parallel

---

## Parallel Example: User Story 1

```bash
# After Phase 2 completes, launch all test updates together:
Task: "Update test_scripts.py assertions to expect new tool ID format"
Task: "Update test_langchain.py assertions to expect new tool ID format"
Task: "Update test_script_langchain_integration.py assertions to expect new tool ID format"
Task: "Add unit tests for validate_tool_id() function"
Task: "Add unit tests for ToolIDValidationError exception"
```

---

## Parallel Example: User Story 2

```bash
# After Phase 2 completes, launch all documentation updates together:
Task: "Update README.md script execution section with new tool ID format"
Task: "Create or update examples/script_execution.py with examples"
Task: "Update docstrings in src/skillkit/core/scripts.py"
Task: "Update docstrings in src/skillkit/integrations/langchain.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Run full test suite
5. Deploy if tests pass

### Incremental Delivery

1. Complete Setup + Foundational → Core format change ready
2. Add User Story 1 → All tests passing (MVP!)
3. Add User Story 2 → Documentation updated → Complete
4. Polish phase → Final validation

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (test updates)
   - Developer B: User Story 2 (documentation updates)
3. Stories complete independently and merge

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each logical group of tasks
- Stop at any checkpoint to validate independently
- **No backward compatibility required**: This is a new feature in v0.3.0, no existing deployments use script tools yet
- **Performance impact**: Validation adds <1ms overhead per tool registration (negligible)
- **LLM provider compatibility**: New format ensures compatibility with all major LLM providers (Anthropic, OpenAI, Google)

---

## Task Summary

**Total Tasks**: 30

**Task Count by Phase**:
- Phase 1 (Setup): 3 tasks
- Phase 2 (Foundational): 6 tasks
- Phase 3 (US1 - Core & Tests): 8 tasks (1 implementation + 7 tests)
- Phase 4 (US2 - Documentation): 6 tasks
- Phase 5 (Polish): 7 tasks

**Test Coverage**: 7 test tasks targeting 70%+ coverage maintenance

**Parallel Opportunities**: 12 tasks marked with [P] can run in parallel

**Independent Test Criteria**:
- US1: Generate tool IDs from test skills, verify format matches `^[a-z0-9-]+__[a-z0-9_]+$` and length ≤60 chars
- US2: Review documentation and run examples, verify all show correct tool ID format

**Suggested MVP Scope**: User Story 1 only (core implementation + tests passing)
