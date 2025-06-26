import re
from .base_page import BasePage
from playwright.sync_api import Page


class DiscoverPage(BasePage):
    def __init__(self, page: Page, base_url: str = "https://tmdb-discover.surge.sh/"):
        super().__init__(page, base_url)
        self.set_test_name("DiscoverPage")

    def click_category(self, category: str):
        self.logger.step(f"Click category: {category}")
        self.click_text(category)

    def wait_for_typeresult(self, validate_fn: callable, type: str):
        self.logger.step(f"Wait for type result: {type}")
        self.wait_for_response(api_match=f"/{type}/popular", validate_fn=validate_fn, timeout=50000)

    def click_for_type(self, type: str):
        self.logger.step(f"Click for type: {type}")
        try:
            self.click_element(".css-tlfecz-indicatorContainer")
        except Exception as e:
            self.logger.error(f"Click for type failed: {type}", e)
            raise
        self.click_text(type)

    def choose_genre(self, genre: str):
        self.logger.step(f"Choose genre: {genre}")
        try:
            self.page.locator("div").filter(has_text=re.compile(r"^Select\.\.\.$")).nth(2).click()
        except Exception as e:
            self.logger.error(f"Choose genre failed: {genre}", e)
            raise
        self.click_text(genre)

    def click_timezone(self, time_zone: str):
        self.logger.step(f"Select time zone: {time_zone}")
        try:
            self.page.locator("div").filter(has_text=re.compile(r"^1900$")).nth(1).click()
        except Exception as e:
            self.logger.error(f"Click time zone failed: {time_zone}", e)
            raise
        self.click_text(time_zone)


    def click_role(self, star: int, timeout: int = 10000):
        self.logger.step(f"Click role star: {star}")
        locator = self.get_element_by_role("radio", name="★ ★", nth=3, timeout=timeout)
        try:
            locator.click(timeout=timeout)
        except Exception as e:
            self.logger.error(f"Click role star failed: {star}", e)
            raise


    def Search(self, key_word: str, timeout: int = 10000):
        self.logger.step(f"Search keyword: {key_word}")
        textbox = self.get_element_by_role("textbox", name="SEARCH", timeout=timeout)
        try:
            textbox.click(timeout=timeout)
            textbox.fill(key_word, timeout=timeout)
            textbox.press("Enter", timeout=timeout)
        except Exception as e:
            self.logger.error(f"Search keyword failed: {key_word}", e)
            raise

    def Pagination(self, pagination, timeout: int = 10000):
        self.logger.step(f"Pagination: {pagination}")
        name = f"Page {pagination}" if isinstance(pagination, int) else pagination
        locator = self.get_element_by_role("button", name=name, timeout=timeout)
        try:
            locator.click(timeout=timeout)
        except Exception as e:
            self.logger.error(f"Pagination failed: {pagination}", e)
            raise
