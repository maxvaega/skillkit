#!/usr/bin/env python3
"""Simple greeting script for skillkit demonstration.

This script demonstrates the basic pattern for skillkit script execution:
1. Read JSON arguments from stdin
2. Access injected environment variables
3. Print human-readable output
4. Exit with appropriate code

Environment Variables (automatically injected by skillkit):
    SKILL_NAME: Name of the skill
    SKILL_BASE_DIR: Absolute path to skill directory
    SKILL_VERSION: Version from skill metadata
    SKILLKIT_VERSION: Current skillkit version
"""

import json
import os
import sys


def main():
    """Execute the greeting demonstration."""
    # Read arguments from stdin (standard skillkit pattern)
    try:
        args = json.load(sys.stdin)
    except json.JSONDecodeError:
        args = {}

    # Extract arguments with defaults
    message = args.get('message', 'Hello!')
    count = args.get('count', 1)
    items = args.get('items', [])

    # Access injected environment variables
    skill_name = os.environ.get('SKILL_NAME', 'unknown')
    skill_base_dir = os.environ.get('SKILL_BASE_DIR', 'unknown')
    skill_version = os.environ.get('SKILL_VERSION', '0.0.0')
    skillkit_version = os.environ.get('SKILLKIT_VERSION', 'unknown')

    # Print formatted output
    print("╔" + "═" * 58 + "╗")
    print(f"║ {'Skillkit Script Execution Demo':^56} ║")
    print("╚" + "═" * 58 + "╝")
    print()
    print(f"✓ Script executed successfully!")
    print(f"✓ Running in: {skill_name} v{skill_version}")
    print(f"✓ Powered by: skillkit v{skillkit_version}")
    print()
    print("Arguments Received:")
    print(f"  • message: \"{message}\"")
    print(f"  • count: {count}")
    print(f"  • items: {items}")
    print()
    print("Environment Variables:")
    print(f"  • SKILL_NAME: {skill_name}")
    print(f"  • SKILL_BASE_DIR: {skill_base_dir}")
    print(f"  • SKILL_VERSION: {skill_version}")
    print(f"  • SKILLKIT_VERSION: {skillkit_version}")
    print()
    print("Output:")
    for i in range(count):
        print(f"  {i + 1}. {message}")

    if items:
        print()
        print("Items List:")
        for item in items:
            print(f"  → {item}")

    print()
    print("─" * 60)
    print("Script execution completed successfully!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
