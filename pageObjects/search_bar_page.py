import time
import logging
from pageObjects.Base_page import BasePage
from selenium.webdriver.common.by import By
from utilities.logger import Logger
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException

logger = Logger.loggen()

class SearchBarPage(BasePage):
    xpath_searchBar = '//input[@type="text"]'
    xpath_suggested_search_length = '//div[@class="left-pane-results-container"]/div'
    xpath_suggested_name = '//div[@role="listitem"]//h2/span'

    def __init__(self, driver):
        super().__init__(driver)

    def enter_search_text(self, search_text):
        try:
            search_bar = self.wait_for_element(By.XPATH, self.xpath_searchBar)
            if search_bar:
                search_bar.send_keys(search_text)
        except Exception as e:
            logger.error(f"An error occurred while entering search text: {e}")
            raise

    def enter_search_text_clear(self):
        try:
            search_bar = self.wait_for_element(By.XPATH, self.xpath_searchBar)

            if search_bar:
                search_bar.clear()
        except Exception as e:
            logger.error(f"An error occurred while clearing search text: {e}")
            raise

    def fetch_length_suggestion_search(self):
        try:
            elements = self.wait_for_elements(By.XPATH, self.xpath_suggested_search_length)
            logger.info(f"Total number of elements found in search suggestions: {len(elements)}")
            return elements
        except Exception as e:
            logger.error(f"An error occurred while fetching suggestions length: {e}")
            raise

    def fetch_suggestions(self):
        """Fetches search suggestions from the page."""
        try:
            # Call fetch_length_suggestion_search method to get the elements
            elements = self.fetch_length_suggestion_search()
            suggestions = []

            for index in range(len(elements)):
                dynamic_xpath = f"//div[@id='sac-suggestion-row-{index + 1}']"
                retry_count = 3
                for attempt in range(retry_count):
                    try:
                        # Wait for the element to be present
                        element = self.wait_for_element(By.XPATH, dynamic_xpath)
                        if element:
                            suggestion_text = element.text.strip()
                            if suggestion_text:
                                suggestions.append(suggestion_text)
                        break  # Break retry loop on success
                    except StaleElementReferenceException:
                        logger.warning(f"StaleElementReferenceException on attempt {attempt + 1}. Retrying...")
                        continue
                    except Exception as e:
                        logger.error(f"Error on attempt {attempt + 1} for element {dynamic_xpath}: {e}")
                        if attempt == retry_count - 1:
                            raise  # Re-raise the exception if we've exhausted retries

            return suggestions

        except Exception as e:
            logger.error(f"An error occurred while fetching suggestions: {e}")
            raise

    def click_first_suggestion(self):
        retries = 3
        try:
            dynamic_xpath = f"//div[@id='sac-suggestion-row-1']"
            attempt = 0
            while attempt < retries:
                try:
                    first_suggestion = self.wait_for_element(By.XPATH, dynamic_xpath)

                    if first_suggestion:
                        first_suggestion.click()
                        return  # Exit the method once clicked
                    else:
                        attempt += 1

                except (TimeoutException, StaleElementReferenceException) as e:
                    attempt += 1
                except Exception as e:
                    attempt += 1

            logger.error(f"Failed to click the first suggestion after {retries} retries.")

        except Exception as e:
            logger.error(f"An error occurred while clicking the first suggestion: {e}")
            raise

    def fetch_suggested_names(self):
        try:
            suggestions = self.wait_for_elements(By.XPATH, self.xpath_suggested_name)
            suggested_names = [suggestion.text for suggestion in suggestions]
            return suggested_names
        except Exception as e:
            logger.error(f"An error occurred while fetching suggested names: {e}")
            raise
