#!/usr/bin/env python3
"""
Test runner script for the CalCount project.
This script sets up the test environment and runs pytest with
appropriate options.
"""

import sys
import subprocess
from pathlib import Path

from dotenv import load_dotenv


def setup_test_environment():
    """Set up test environment variables."""
    load_dotenv()


def run_tests():
    """Run pytest with appropriate options."""
    setup_test_environment()

    # Get the project root directory
    project_root = Path(__file__).parent

    # pytest command with options
    cmd = [
        sys.executable, "-m", "pytest",
        str(project_root / "tests"),
        "-v",
        "--tb=short",
        "--cov=.",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--cov-fail-under=80",
    ]

    # Add additional arguments if provided
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])

    print("Running tests with command:", " ".join(cmd))
    print("=" * 50)

    # Run the tests
    result = subprocess.run(cmd, cwd=project_root)

    return result.returncode


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
