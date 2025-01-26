import time
import pytest
from pageObjects.search_bar_page import SearchBarPage
from utilities.logger import Logger

logger = Logger.loggen()


class TestAmazonSearchBar:
    @pytest.mark.sahil
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.run(priority=1)  # Highest priority
    @pytest.mark.parametrize("text_string", ['Iphone 13'])
    def test_search_suggestions(self, setup, text_string):
        self.driver = setup
        search_page = SearchBarPage(self.driver)
        search_page.enter_search_text(text_string)  # Pass text_string here
        suggestions = search_page.fetch_suggestions()
        assert len(suggestions) > 0, "Suggestions were not fetched for a valid search input."

        failure_messages = []
        for text in suggestions:
            try:
                if text_string.lower() not in text.lower():
                    failure_messages.append(f"Wrong suggestion in search bar, fetched suggestion is: {text}")
            except AssertionError as e:
                failure_messages.append(str(e))

        if failure_messages:
            logger.error("\n".join(failure_messages))
            assert False, "One or more wrong suggestions found. Check the logs for details."

    @pytest.mark.sahil
    @pytest.mark.regression
    @pytest.mark.run(priority=2)  # Second priority
    @pytest.mark.parametrize("text_string", ['Iphone 15'])
    def test_valid_search_input(self, setup, text_string):
        self.driver = setup
        search_page = SearchBarPage(self.driver)
        search_page.enter_search_text(text_string)
        suggestions = search_page.fetch_suggestions()
        assert len(suggestions) > 0, "Suggestions were not fetched for a valid search input."

    @pytest.mark.sahil
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.run(priority=3)  # Third priority
    def test_empty_search_input(self, setup):
        self.driver = setup
        search_bar_page = SearchBarPage(self.driver)
        search_bar_page.enter_search_text("")
        suggestions = search_bar_page.fetch_suggestions()
        assert len(suggestions) == 0, "Suggestions should not be fetched for an empty search input."

    @pytest.mark.sahil
    @pytest.mark.run(priority=4)  # Fourth priority
    def test_invalid_search_input(self, setup):
        self.driver = setup
        search_bar_page = SearchBarPage(self.driver)
        search_bar_page.enter_search_text("asdkfjasdf")
        suggestions = search_bar_page.fetch_suggestions()
        assert len(suggestions) == 0, "Suggestions should not be fetched for an invalid search input."

    @pytest.mark.sahil
    @pytest.mark.run(priority=5)  # Fifth priority
    @pytest.mark.parametrize("text_string", ['Iphone 15'])
    def test_fetched_suggestions(self, setup, text_string):
        self.driver = setup
        search_bar_page = SearchBarPage(self.driver)
        search_bar_page.enter_search_text(text_string)
        suggestions = search_bar_page.fetch_suggestions()
        assert len(suggestions) > 0, "Suggestions list is empty after searching for a valid query."
        failure_messages = []  # List to collect any failure messages

        if suggestions:
            search_bar_page.click_first_suggestion()
            suggested_names = search_bar_page.fetch_suggested_names()

            for text in suggested_names:
                try:
                    # Check for case-insensitive match
                    if text_string.lower() not in text.lower():
                        failure_messages.append(f"Wrong suggestion in main page, fetched suggestion is: {text}")
                except AssertionError as e:
                    failure_messages.append(str(e))

        if failure_messages:
            logger.error("\n".join(failure_messages))
            assert False, "One or more wrong suggestions found. Check the logs for details."

    @pytest.mark.sahil
    @pytest.mark.run(priority=6)  # Sixth priority
    def test_click_first_suggestion_URL(self, setup):
        self.driver = setup
        search_bar_page = SearchBarPage(self.driver)
        search_bar_page.enter_search_text("Iphone 15")
        search_bar_page.click_first_suggestion()
        assert "iphone+15".lower() in search_bar_page.driver.current_url.lower(), "URL does not match after clicking the first suggestion"

    @pytest.mark.sahil
    @pytest.mark.run(priority=7)  # Seventh priority
    def test_string_with_spaces(self, setup):
        self.driver = setup
        search_bar_page = SearchBarPage(self.driver)
        search_bar_page.enter_search_text("  Iphone 15  ")
        suggestions = search_bar_page.fetch_suggestions()
        assert len(suggestions) > 0, "Suggestions should be fetched even with spaces in the input."

    @pytest.mark.run(priority=8)
    @pytest.mark.parametrize("text_string", ['Iphone 15 @#$%', 'Laptop #123'])
    def test_special_characters_in_search(self, setup, text_string):
        self.driver = setup
        search_page = SearchBarPage(self.driver)
        search_page.enter_search_text(text_string)
        suggestions = search_page.fetch_suggestions()
        assert len(suggestions) > 0, f"No suggestions fetched for search input with special characters: {text_string}"

    @pytest.mark.run(priority=9)
    def test_long_search_input(self, setup):
        long_search_text = "Iphone 15 with 128GB storage and long description included to test the search input handling behavior"
        self.driver = setup
        search_page = SearchBarPage(self.driver)
        search_page.enter_search_text(long_search_text)
        suggestions = search_page.fetch_suggestions()
        assert len(suggestions) == 0, "Suggestions were not fetched for long search input."

    @pytest.mark.run(priority=11)
    @pytest.mark.parametrize("text_string", ['Iphone 15 pro max'])
    def test_multiple_words_in_search(self, setup, text_string):
        self.driver = setup
        search_page = SearchBarPage(self.driver)
        search_page.enter_search_text(text_string)
        suggestions = search_page.fetch_suggestions()
        assert len(suggestions) > 0, f"No suggestions fetched for multi-word search: {text_string}"

    @pytest.mark.run(priority=12)
    @pytest.mark.parametrize("text_string", ['Iphone 15 256GB', 'Iphone 15 64GB'])
    def test_suggestions_with_numbers(self, setup, text_string):
        self.driver = setup
        search_page = SearchBarPage(self.driver)
        search_page.enter_search_text(text_string)
        suggestions = search_page.fetch_suggestions()
        assert len(suggestions) > 0, f"No suggestions fetched for search input with numbers: {text_string}"

    @pytest.mark.run(priority=14)
    @pytest.mark.parametrize("text_string", ['Iphone 15', 'IPHONE 15', 'iPhone 15'])
    def test_case_insensitive_search(self, setup, text_string):
        self.driver = setup
        search_page = SearchBarPage(self.driver)
        search_page.enter_search_text(text_string)
        suggestions = search_page.fetch_length_suggestion_search()
        assert len(suggestions) > 0, f"No suggestions fetched for case-insensitive search: {text_string}"

    @pytest.mark.run(priority=15)
    @pytest.mark.parametrize("text_string", ['Iphone 13', 'Iphone 15', 'Iphone 12'])
    def test_partial_match_suggestions(self, setup, text_string):
        self.driver = setup
        search_page = SearchBarPage(self.driver)
        search_page.enter_search_text(text_string)
        suggestions = search_page.fetch_suggestions()
        assert len(suggestions) > 0, f"No suggestions fetched for partial search: {text_string}"
