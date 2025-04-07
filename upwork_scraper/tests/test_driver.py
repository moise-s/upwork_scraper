# tests/test_driver.py

import os
from unittest.mock import Mock

import pytest
from selenium.webdriver.remote.webelement import WebElement

from upwork_scraper.driver import ChromeDriver, DriverManager


@pytest.fixture
def mock_chrome_driver():
    return ChromeDriver()


def test_create_chrome_driver(mock_chrome_driver):
    assert mock_chrome_driver is not None


def test_go_to_url(mock_chrome_driver):
    mock_chrome_driver.go_to_url("https://example.com/")
    assert mock_chrome_driver._driver.current_url == "https://example.com/"


def test_enter_text_when_loaded(mock_chrome_driver):
    element_content = "example_input"
    text = "test_text"
    mock_chrome_driver._get_element_by_id = Mock(return_value=Mock(spec=WebElement))
    mock_chrome_driver.enter_text_when_loaded(element_content, text)
    mock_chrome_driver._get_element_by_id.assert_called_once_with(element_content)


def test_click_element(mock_chrome_driver):
    element_content = "example_button"
    mock_chrome_driver._get_element_by_id = Mock(return_value=Mock(spec=WebElement))
    mock_chrome_driver.click_element(element_content)
    mock_chrome_driver._get_element_by_id.assert_called_once_with(element_content)


def test_get_profile_link(mock_chrome_driver):
    pattern = "example_pattern"
    mock_chrome_driver._driver.find_element = Mock(return_value=Mock(spec=WebElement))
    link = mock_chrome_driver.get_profile_link(pattern)
    assert link is not None


def test_is_element_present(mock_chrome_driver):
    element_content = "example_element"
    mock_chrome_driver._driver.find_element = Mock(return_value=Mock(spec=WebElement))
    assert mock_chrome_driver.is_element_present(element_content) is True


def test_is_element_present_by_xpath(mock_chrome_driver):
    element_content = "example_element_xpath"
    mock_chrome_driver._driver.find_element = Mock(return_value=Mock(spec=WebElement))
    assert mock_chrome_driver.is_element_present_by_xpath(element_content) is True


def test_create_driver_manager(mock_chrome_driver):
    manager = DriverManager(mock_chrome_driver)
    assert manager is not None
    assert manager.driver == mock_chrome_driver
    assert manager.username == os.getenv("USERNAME")
    assert manager.password == os.getenv("PASSWORD")
    assert manager.secret_answer == os.getenv("SECRET_ANSWER")
