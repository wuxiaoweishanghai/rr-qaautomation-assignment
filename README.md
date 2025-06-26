UI Automation Framework with Playwright, Pytest, and Allure
This is a Python-based UI automation framework built with Playwright, Pytest, and Allure. It includes:

A custom StepLogger for unified logging to console, file, and Allure reports

A reusable BasePage class implementing common page actions with logging and Allure integration

Support for HTTP response validation during UI tests

Screenshot capturing on test failure (configured separately in conftest.py)

Install
pip -r requirements.txt
playwright install
playwright install chromium
brew install allure

Running Tests

python run_tests.py --build-name="Jenkins_1234" --build-url="http://jenkins/job/1234"
Generating Allure Reports
allure serve ./allure-results

Notes

Customize build-name and build-url to include Jenkins or CI build information in Allure EXECUTORS section.

Logs are saved to the logs/ directory, with filenames timestamped by hour and test name.

Screenshots and HTTP response attachments are handled in test hooks (see conftest.py).