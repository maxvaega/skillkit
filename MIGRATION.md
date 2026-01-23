# Migration Guide: skillkit v0.4 → v0.5

**Status**: Work in Progress
**Target Release**: v0.5.0
**Breaking Changes**: Yes (Major Version Bump)

---

## Overview

This guide will help you migrate from skillkit v0.4 to v0.5. The v0.5 release removes proactive script discovery to align with official Claude skills design, adopting an instruction-based execution pattern instead.

**Key Changes**:
- Script discovery removed (`skill.scripts` property)
- Script tool generation removed (`create_script_tools()`)
- ShellTool integration for instruction-based execution
- Direct execution API preserved for programmatic use

---

## Quick Links

- **Breaking Changes**: See section below
- **Migration Steps**: Follow the 5-step process
- **Troubleshooting**: Common errors and solutions
- **Full API Diff**: See `specs/001-align-claude-skills-design/contracts/api-changes.md`

---

**Note**: Detailed migration content will be added during implementation of User Story 4.

For now, refer to:
- `specs/001-align-claude-skills-design/quickstart.md` - Complete examples
- `specs/001-align-claude-skills-design/contracts/api-changes.md` - API changes
- `specs/001-align-claude-skills-design/research.md` - Design rationale
