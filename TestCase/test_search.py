import allure
import pytest
from pages.discover import DiscoverPage

def validate_status_and_results(body):
    assert isinstance(body, dict), "Response body is not a dict"
    assert "results" in body, "'results' key not in response"
    assert isinstance(body["results"], list), "'results' is not a list"
    assert len(body["results"]) > 0, "'results' list is empty"

@pytest.mark.parametrize("search_word", ["Vrigin", "Vrigin", "vri"])
@allure.feature("Discover Search Fuction")
def test_Search(page, search_word):
    discover = DiscoverPage(page)
    discover.goto(path = "")
    discover.Search(search_word)
    discover.wait_for_response(api_match= "search/movie", validate_fn=validate_status_and_results)







