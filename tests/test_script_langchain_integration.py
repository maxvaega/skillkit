"""This test file has been removed in v0.5.0.

Script tool generation has been removed from the LangChain integration.
Skills now use instruction-based execution with ShellTool instead of
automatically generated script tools.

Tests removed:
- test_create_script_tools_basic
- test_create_script_tools_descriptions
- test_script_tool_invocation_success
- test_script_tool_invocation_failure
- test_create_langchain_tools_includes_scripts
- test_script_tool_with_empty_description

For script execution testing, see:
- tests/test_manager.py (execute_skill_script tests)
- tests/test_script_executor.py (direct executor tests)

For LangChain integration testing, see:
- tests/test_langchain_integration.py (prompt-based tools only)
"""
