"""Script Execution Example for skillkit v0.3.0

This example demonstrates:
1. Basic script execution with arguments
2. Environment variable injection (SKILL_NAME, SKILL_BASE_DIR, SKILL_VERSION, SKILLKIT_VERSION)
3. Error handling for script failures
4. Timeout management
5. Tool restriction enforcement

Prerequisites:
    - skillkit v0.3.0+
    - Python 3.10+
    - Example skills with scripts in examples/skills/

Usage:
    python examples/script_execution.py
"""

import asyncio
import json
from pathlib import Path

from skillkit import SkillManager
from skillkit.core.exceptions import (
    ScriptNotFoundError,
    ToolRestrictionError,
    InterpreterNotFoundError,
)


async def main():
    """Run script execution examples."""
    print("=" * 80)
    print("skillkit v0.3.0 - Script Execution Examples")
    print("=" * 80)
    print()

    # Discover skills in examples directory
    examples_dir = Path(__file__).parent / "skills"

    # Initialize SkillManager with script support
    manager = SkillManager(
        default_script_timeout=30,
        project_skill_dir=examples_dir
    )

    await manager.adiscover()
    skill_metadata_list = manager.list_skills()

    print(f"✓ Discovered {len(skill_metadata_list)} skills from {examples_dir}")
    print()

    # Example 1: Basic Script Execution
    print("-" * 80)
    print("Example 1: Basic Script Execution with Environment Variables")
    print("-" * 80)
    print()

    try:
        # Find demo-skill for demonstration (falls back to any skill with scripts)
        skill_with_scripts = None
        for metadata in skill_metadata_list:
            if metadata.name == 'demo-skill':
                skill_with_scripts = manager.load_skill(metadata.name)
                break

        # Fallback: find any skill with scripts
        if not skill_with_scripts:
            for metadata in skill_metadata_list:
                skill = manager.load_skill(metadata.name)
                if skill.scripts:
                    skill_with_scripts = skill
                    break

        if skill_with_scripts:
            print(f"Using skill: {skill_with_scripts.metadata.name}")
            print(f"Available scripts: {[s.name for s in skill_with_scripts.scripts]}")
            print()

            # Execute the first script
            script = skill_with_scripts.scripts[0]
            print(f"Executing script: {script.name}")
            print(f"Script type: {script.script_type}")
            print(f"Description: {script.description or 'No description'}")
            print()

            # Prepare arguments
            arguments = {
                "message": "Hello from skillkit!",
                "count": 3,
                "items": ["apple", "banana", "cherry"]
            }

            print(f"Arguments: {json.dumps(arguments, indent=2)}")
            print()

            # Execute the script
            result = manager.execute_skill_script(
                skill_name=skill_with_scripts.metadata.name,
                script_name=script.name,
                arguments=arguments,
                timeout=10
            )

            # Display results
            print("Execution Result:")
            print(f"  Exit Code: {result.exit_code}")
            print(f"  Success: {result.success}")
            print(f"  Execution Time: {result.execution_time_ms:.2f}ms")
            print()

            if result.success:
                print("Standard Output:")
                print("-" * 40)
                print(result.stdout)
                print("-" * 40)
            else:
                print("Standard Error:")
                print("-" * 40)
                print(result.stderr)
                print("-" * 40)

            # Check for truncation
            if result.stdout_truncated or result.stderr_truncated:
                print()
                print("⚠️  Output was truncated (exceeded 10MB limit)")

            # Check for signals
            if result.signaled:
                print()
                print(f"⚠️  Script was terminated by signal: {result.signal} ({result.signal_number})")

            print()
        else:
            print("⚠️  No skills with scripts found in examples directory")
            print()

    except ScriptNotFoundError as e:
        print(f"❌ Script not found: {e}")
        print()
    except InterpreterNotFoundError as e:
        print(f"❌ Interpreter not found: {e}")
        print("   Make sure the required interpreter is installed and in PATH")
        print()
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        print()

    # Example 2: Environment Variable Demonstration
    print("-" * 80)
    print("Example 2: Environment Variables Injected into Scripts")
    print("-" * 80)
    print()

    print("The following environment variables are automatically injected:")
    print("  - SKILL_NAME: Name of the skill")
    print("  - SKILL_BASE_DIR: Absolute path to skill directory")
    print("  - SKILL_VERSION: Version from skill metadata")
    print("  - SKILLKIT_VERSION: Current skillkit version")
    print()

    print("Scripts can access these variables to:")
    print("  - Locate files relative to skill directory")
    print("  - Include skill context in logs")
    print("  - Version-specific behavior")
    print()

    print("Example Python script:")
    print("-" * 40)
    print("""import os
import sys
import json

# Read arguments from stdin
args = json.load(sys.stdin)

# Access environment variables
skill_name = os.environ['SKILL_NAME']
skill_base = os.environ['SKILL_BASE_DIR']
skill_version = os.environ.get('SKILL_VERSION', '0.0.0')
skillkit_version = os.environ['SKILLKIT_VERSION']

# Use environment context
print(f"Running in skill: {skill_name} v{skill_version}")
print(f"Skill directory: {skill_base}")
print(f"Powered by skillkit v{skillkit_version}")
print(f"Arguments: {args}")
""")
    print("-" * 40)
    print()

    # Example 3: Error Handling
    print("-" * 80)
    print("Example 3: Error Handling - Script Not Found")
    print("-" * 80)
    print()

    try:
        if skill_with_scripts:
            # Try to execute a non-existent script
            print(f"Attempting to execute script named 'nonexistent_script' in skill: {skill_with_scripts.metadata.name}..")
            print()
            result = manager.execute_skill_script(
                skill_name=skill_with_scripts.metadata.name,
                script_name="nonexistent_script",
                arguments={},
                timeout=10
            )
    except ScriptNotFoundError as e:
        print(f"✓ Caught expected error: {e}")
        print()

    # Example 4: Timeout Management
    print("-" * 80)
    print("Example 4: Timeout Management")
    print("-" * 80)
    print()

    print("Scripts are executed with timeout enforcement:")
    print("  - Default timeout: 30 seconds (configurable)")
    print("  - Custom timeout per execution")
    print("  - Timeout results in exit code 124")
    print()

    print("Example with custom timeout:")
    print("""
result = manager.execute_skill_script(
    skill_name='pdf-extractor',
    script_name='extract',
    arguments={'file': 'large_document.pdf'},
    timeout=60  # 60-second timeout for large files
)

if result.timeout:
    print(f"Script timed out after {timeout}s")
""")
    print()

    # Summary
    print("=" * 80)
    print("Summary: Key Features")
    print("=" * 80)
    print()
    print("✓ Scripts detected automatically from skill directories")
    print("✓ Arguments passed as JSON via stdin")
    print("✓ Environment variables injected for context")
    print("✓ Timeout enforcement prevents infinite loops")
    print("✓ Output captured up to 10MB per stream")
    print("✓ Security validation (path traversal, permissions)")
    print("✓ Tool restriction enforcement")
    print("✓ Cross-platform support (Linux, macOS, Windows)")
    print()
    print("For LangChain integration, see: examples/langchain_agent.py")
    print("For async usage patterns, see: examples/async_usage.py")
    print()


if __name__ == "__main__":
    asyncio.run(main())
