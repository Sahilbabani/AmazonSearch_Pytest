import pytest
from selenium import webdriver
import os
from datetime import datetime
import logging
from utilities.readProperties import ReadConfig
from utilities.logger import Logger
from datetime import datetime

logger = Logger.loggen()

baseUrl = ReadConfig.getApplicationUrl()

def pytest_configure(config):
    report_folder = os.path.join(os.path.abspath(os.curdir), "reports")
    current_date_format = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    os.makedirs(report_folder, exist_ok=True)  # Ensure the folder exists
    report_file = os.path.join(
        report_folder, current_date_format + ".html"
    )
    config.option.htmlpath = report_file
    logger.info(f"Reports will be saved to: {report_file}")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests on")

@pytest.fixture()
def setup(request):

    browser_name = request.config.getoption("--browser")
    if browser_name == "chrome":
        driver = webdriver.Chrome()
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Chrome()
        logger.WARN(f"Unsupported browser: {browser_name}, hence opening default browser that is Chrome Browser")
        raise ValueError(f"Unsupported browser: {browser_name}")

    logger.info("Setting up the WebDriver environment...")
    try:
        driver.maximize_window()

        driver.get(baseUrl)

        logger.info("WebDriver setup completed successfully.")

        # Attach the driver to the test item
        request.node.driver = driver

        yield driver
    except Exception as e:
        logger.error(f"Error during WebDriver setup: {e}")
    finally:
        logger.info("Tearing down the WebDriver environment...")
        driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots on test failure."""
    outcome = yield
    report = outcome.get_result()


    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)
        if driver:
            screenshots_folder = os.path.join(os.path.abspath(os.curdir), "screenshots")
            os.makedirs(screenshots_folder, exist_ok=True)  # Ensure the folder exists
            screenshot_path = os.path.join(
                screenshots_folder,
                f"{item.name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png",
            )
            driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved to: {screenshot_path}")
        else:
            logger.info(f"No driver found inside calling function")