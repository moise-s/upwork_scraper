"""A module for managing the Webdriver."""

import os
from typing import Any

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from argyle_upwork.logger import logger


class ChromeDriver:
    """A class to manage the Selenium webdriver for Google Chrome."""

    def __init__(self, headless: bool = True):
        """Initialize the ChromeDriver with the specified configuration."""
        self.timeout: int = 10
        self.timeout_for_checking_presence: int = 3
        self.headless = headless
        self._driver = self._create_driver()
        self.login_url: str = "https://www.upwork.com/ab/account-security/login"
        self.homepage_url: str = "https://www.upwork.com/nx/find-work/best-matches"
        self.contact_info_url: str = (
            "https://www.upwork.com/freelancers/settings/contactInfo"
        )
        self.profile_page_url: str = "https://www.upwork.com/freelancers/~01b5ffe1df46c24d0e"  # correct method to obtain this url

    def _create_driver(self) -> webdriver.Chrome:
        """Create a new instance of the Chrome webdriver with the specified options."""
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs",
            {
                "profile.default_content_settings.popups": 0,
            },
        )
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 "
            "Safari/537.36"
        )

        if self.headless:
            options.add_argument("--headless")

        return webdriver.Chrome(
            options=options, service=Service(ChromeDriverManager().install())
        )

    def go_to_url(self, url: str) -> None:
        """Navigate the ChromeDriver to the specified URL."""
        self._driver.get(url)

    def enter_text_when_loaded(self, element_content: str, text: str) -> None:
        """Enter text after element is loaded."""
        self._wait_until_loaded(EC.element_to_be_clickable((By.ID, element_content)))
        element = self._get_element_by_id(element_content)
        element.send_keys(text)

    def click_element(self, element_content: str) -> None:
        """Click the specified element."""
        self._wait_until_loaded(EC.element_to_be_clickable((By.ID, element_content)))
        element = self._get_element_by_id(element_content)
        element.click()

    def _wait_until_loaded(self, condition: Any) -> None:
        """Wait until the specified condition is loaded."""
        try:
            WebDriverWait(self._driver, self.timeout).until(condition)
        except TimeoutException:
            logger.error("Timed out waiting for condition.")

    def _get_element_by_id(self, element_content: str) -> WebElement:
        """Get the specified element."""
        return self._driver.find_element(By.ID, element_content)

    def _get_element_by_xpath(self, element_content):
        """Get the specified element."""
        return self._driver.find_element(By.XPATH, element_content)

    def is_logged(self) -> bool:
        """Check if the user is logged in."""
        try:
            WebDriverWait(self._driver, self.timeout).until(
                EC.presence_of_element_located((By.ID, "nav-notifications-label"))
            )
            return True
        except TimeoutException:
            return False

    def is_at_homepage(self) -> bool:
        """Check if the ChromeDriver is at the homepage."""
        try:
            WebDriverWait(self._driver, self.timeout).until(
                EC.url_to_be(self.homepage_url)
            )
            WebDriverWait(self._driver, self.timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "[data-test='announcements']")
                )
            )
            return True
        except TimeoutException:
            return False

    def is_at_contact_info_page(self) -> bool:
        """Check if the ChromeDriver is at the contact info page."""
        try:
            WebDriverWait(self._driver, self.timeout).until(
                EC.url_to_be(self.contact_info_url)
            )
            WebDriverWait(self._driver, self.timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "[data-test='settings-nav']")
                )
            )
            return True
        except TimeoutException:
            return False

    def is_at_profile_page(self) -> bool:
        """Check if the ChromeDriver is at the profile page."""
        try:
            WebDriverWait(self._driver, self.timeout).until(
                EC.url_contains("www.upwork.com/freelancers/~")
            )
            return True
        except TimeoutException:
            return False

    def get_page_source(self):
        """Get the page source of the current webpage."""
        return self._driver.page_source

    def is_element_present(self, element_content: str) -> bool:
        """Check if the element is present."""
        try:
            WebDriverWait(self._driver, self.timeout_for_checking_presence).until(
                EC.presence_of_element_located((By.ID, element_content))
            )
            return True
        except TimeoutException:
            return False

    def is_element_present_by_xpath(self, element_content: str) -> bool:
        """Check if the element is present."""
        try:
            WebDriverWait(self._driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, element_content))
            )
            return True
        except TimeoutException:
            return False


class DriverManager:
    """Class to handle same Driver within scanning classes."""

    def __init__(self, driver: ChromeDriver):
        """Initialize the DriverManager with the specified ChromeDriver instance."""
        self.driver = driver
        self.username: str = os.getenv("USERNAME")
        self.password: str = os.getenv("PASSWORD")
        self.secret_answer: str = os.getenv("SECRET_ANSWER")
