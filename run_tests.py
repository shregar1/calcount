"""
Test runner script for the CalCount project.
Sets up the test environment and runs pytest with coverage and
reporting options.
"""
import sys
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger


def setup_test_environment():
    """
    Set up test environment variables using dotenv.
    """
    logger.info("Setting up test environment variables")
    load_dotenv()


def run_tests():
    """
    Run pytest with coverage and reporting options.
    Returns:
        int: The exit code from pytest.
    """
    logger.info("Starting test run")
    setup_test_environment()

    project_root = Path(__file__).parent

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

    if len(sys.argv) > 1:
        logger.info(f"Passing additional arguments to pytest: {sys.argv[1:]}")
        cmd.extend(sys.argv[1:])

    logger.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=project_root)
    logger.info(f"Test run completed with exit code {result.returncode}")
    return result.returncode


if __name__ == "__main__":
    """
    Main entry point for the test runner script.
    """
    exit_code = run_tests()
    sys.exit(exit_code)
