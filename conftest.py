# conftest.py
import json
import os
import allure
from datetime import datetime
import pytest
from _pytest.reports import TestReport
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption("--build-name", action="store", default="build-001", help="Jenkins build name")
    parser.addoption("--build-url", action="store", default="http://ci.example.com/1234", help="Jenkins build URL")

@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        browser.close()

@pytest.fixture
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()

response_store = {}

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook triggered after each test step (setup/call/teardown).
    On test failure, capture screenshot, attach to Allure,
    include response body and log content if available.
    """
    outcome = yield
    report: TestReport = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    test_name = item.name.replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Screenshot
    page = item.funcargs.get("page", None)
    if page:
        try:
            screenshot_path = os.path.join("screenshots", f"{test_name}_{timestamp}.png")
            page.screenshot(path=screenshot_path, full_page=True)
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name=f"{test_name}_screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print(f"[WARN] Screenshot failed: {e}")

    # HTTP Response
    response = response_store.get(item.name)
    if response:
        try:
            body = response.text() if callable(response.text) else str(response)
            allure.attach(body, name="HTTP Response", attachment_type=allure.attachment_type.JSON)
        except Exception as e:
            allure.attach(f"Response body attach failed: {e}", name="Error",
                          attachment_type=allure.attachment_type.TEXT)

    # Execution log
    log_path = f"logs/{test_name}.log"
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            allure.attach(f.read(), name="Execution Log", attachment_type=allure.attachment_type.TEXT)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):

    env_info = {
        "env": "testing",
        "browser": "chromium",
        "base_url": "https://tmdb-discover.surge.sh/",
    }

    result_dir = os.getenv("ALLURE_RESULTS_DIR", "allure-results")
    os.makedirs(result_dir, exist_ok=True)

    with open(os.path.join(result_dir, "environment.properties"), "w") as f:
        for key, value in env_info.items():
            f.write(f"{key}={value}\n")

    build_name = os.getenv("BUILD_NAME")
    build_url = os.getenv("BUILD_URL")

    executor_info = {
        "name": "Automation Run",
        "type": "Automation",
        "reportName": "Local Allure Report",
        "url": "https://tmdb-discover.surge.sh/",
        "buildName": build_name,
        "buildUrl": build_url,
    }

    with open(os.path.join(result_dir, "executor.json"), "w", encoding="utf-8") as f:
        json.dump(executor_info, f, indent=4)
