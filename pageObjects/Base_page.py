from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from utilities.logger import Logger

logger = Logger.loggen()

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, value, timeout=30):
        """Waits for a single element to appear in the DOM."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            logger.error(f"Timeout waiting for element {by}='{value}'.")
        except Exception as e:
            logger.error(f"Unexpected error while waiting for element {by}='{value}': {e}")
        return None

    def wait_for_elements(self, by, value, timeout=10):
        """Waits for all elements to appear in the DOM."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
        except TimeoutException:
            logger.error(f"Timeout waiting for elements {by}='{value}'.")
        except Exception as e:
            logger.error(f"Unexpected error while waiting for elements {by}='{value}': {e}")
        return []