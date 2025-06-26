import allure
import pytest
from pages.discover import DiscoverPage

def validate_status_and_results(body):
    assert isinstance(body, dict), "Response body is not a dict"
    assert "results" in body, "'results' key not in response"
    assert isinstance(body["results"], list), "'results' is not a list"
    assert len(body["results"]) > 0, "'results' list is empty"

@pytest.mark.parametrize("pagination", [4, "...", 51503])
@allure.feature("Discover Search Fuction")
def test_Pagination(page, pagination: int):
    discover = DiscoverPage(page)
    discover.goto(path = "")
    discover.Pagination(pagination)
    page.get_by_role("button", name="...").click()
    discover.wait_for_response(api_match= "/movie/popular", validate_fn=validate_status_and_results)







