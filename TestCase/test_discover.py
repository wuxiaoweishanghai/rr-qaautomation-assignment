import allure
import pytest
from pages.discover import DiscoverPage

def validate_status_and_results(body):
    assert isinstance(body, dict), "Response body is not a dict"
    assert "results" in body, "'results' key not in response"
    assert isinstance(body["results"], list), "'results' is not a list"
    assert len(body["results"]) > 0, "'results' list is empty"


@pytest.mark.parametrize("category", ["Trend", "Newest", "Top rated"])
@allure.feature("Discover Page Category")
def test_discover_category(page, category):
    discover = DiscoverPage(page)
    discover.goto(path = "")
    discover.click_category(category)
    discover.wait_for_response(api_match="/movie/", validate_fn=validate_status_and_results,)