# Pytest Search Framework

This is a test automation framework built using **pytest** for testing search functionality on a web application. The framework is structured for easy configuration and extensibility.

## Project Structure

TestProject/
├── Configuration/
│   └──config.ini
├── logs/
├── pageObjects/
│   └── search_bar_page.py
├── reports/
├── screenshots/
├── testCases/
│   └── conftest.py
│   └── test_search.py
├── utilities/
│   └── logger.py
│   └── readProperties.py
├── TestCase.xlsx
└── requirements.txt


## Features

- **Page Object Model (POM)** for maintainable and scalable tests.
- Custom **pytest fixtures** and configurations for better test control.
- **Logging** for capturing detailed test execution information.
- **Screenshots** for failed test cases to aid debugging.
- **Reports** to summarize test execution results.



## Configuration

The configuration settings can be found in the `Configuration/config.ini` file. This includes settings like base URL, browser type, and other environment-specific configurations.

Example configuration:
```ini
[Settings]
base_url = https://example.com
browser = chrome


## Running Specific Test Cases
pytest testCases/test_search.py
pytest testCases/test_search.py::test_search_functionality
refer resource/cmd_to_run file to execte multiple test cases.

