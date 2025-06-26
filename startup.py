# run_tests.py
import pytest
import os
import argparse

if __name__ == "__main__":
    # Parse arguments from CLI
    parser = argparse.ArgumentParser(description="Run tests and generate Allure report.")
    parser.add_argument("--build-name", help="Build name from Jenkins", default="build-001")
    parser.add_argument("--build-url", help="Build URL from Jenkins", default="http://ci.example.com/1234")
    args = parser.parse_args()

    # # Set env vars to pass to conftest.py
    # os.environ["BUILD_NAME"] = args.build_name
    # os.environ["BUILD_URL"] = args.build_url

    # Allure result directory
    result_dir = os.path.abspath("./allure-results")
    os.makedirs(result_dir, exist_ok=True)

    # Run pytest
    exit_code = pytest.main([
        "--alluredir", result_dir,
        "TestCase"  # Or your test path
    ])
    exit(exit_code)
