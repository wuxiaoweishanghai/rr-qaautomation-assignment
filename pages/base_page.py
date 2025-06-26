import json
import allure
from common.logger import StepLogger
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page, base_url: str = ""):
        self.page = page
        self.base_url = base_url
        self.test_name = ""

    def set_test_name(self, name: str):
        self.test_name = name
        self.logger = StepLogger(test_name=name, page=self.page)

    def goto(self, path: str):
        self.logger.step(f"Goto URL: {self.base_url + path}")
        try:
            self.page.goto(self.base_url + path)
        except Exception as e:
            self.logger.error("Navigation failed", e)
            raise

    def click_element(self, selector: str, timeout: int = 10000):
        self.logger.step(f"Click element: {selector}")
        try:
            locator = self.page.locator(selector).first
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
        except Exception as e:
            self.logger.error(f"Click failed: {selector}", e)
            raise

    def click_text(self, text: str, timeout: int = 10000):
        self.logger.step(f"Click text: {text}")
        try:
            self.page.get_by_text(text, exact=True).click(timeout=timeout)
        except Exception as e:
            self.logger.error(f"Click text failed: {text}", e)
            raise

    def assert_text(self, selector: str, expected: str):
        self.logger.step(f"Assert text at {selector} == {expected}")
        try:
            actual = self.page.locator(selector).inner_text()
            assert actual == expected, f"Expected '{expected}', but got '{actual}'"
        except Exception as e:
            self.logger.error(f"Assertion failed: {selector}", e)
            raise

    def wait_for_response(self, api_match: str, validate_fn: callable = None, timeout: int = 10000):
        self.logger.step(f"Wait for response matching: {api_match}")
        try:
            with self.page.expect_response(lambda res: api_match in res.url, timeout=timeout) as response_info:
                pass
            response = response_info.value

            allure.attach(str(response.status), name="HTTP Status", attachment_type=allure.attachment_type.TEXT)

            try:
                body = response.json()
                allure.attach(
                    json.dumps(body, indent=2, ensure_ascii=False),
                    name="Response JSON",
                    attachment_type=allure.attachment_type.JSON
                )
            except Exception as e:
                allure.attach(
                    f"Failed to parse JSON: {e}",
                    name="Response Body Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                body = {}

            if validate_fn:
                self.logger.step("Validate response body")
                validate_fn(body)

            return response
        except Exception as e:
            self.logger.error("Wait for response failed", e)
            raise

    def get_element_by_role(self, role: str, name: str, nth: int = None, timeout: int = 10000):
        self.logger.step(f"Get by role: {role}, name: {name}, nth: {nth}")
        try:
            locator = self.page.get_by_role(role, name=name)
            if nth is not None:
                locator = locator.nth(nth)
            locator.wait_for(timeout=timeout)
            return locator
        except Exception as e:
            self.logger.error(f"Get element by role failed: {role}, {name}", e)
            raise
