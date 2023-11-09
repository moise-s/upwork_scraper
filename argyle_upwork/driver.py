from typing import Any

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from argyle_upwork.logger import logger


class ChromeDriver:
    """
    A class to manage the Selenium webdriver for Google Chrome.
    """

    timeout: int = 10

    def __init__(self, headless: bool = False):
        """
        Initializes the Driver class with specified parameters.

        Parameters
        ----------
        headless : bool, optional
            Starts the browser in headless mode if True, by default True.
        """
        self.headless = headless
        self._driver = self._create_driver()

    def _create_driver(self) -> webdriver.Chrome:
        """
        Creates and configures the Chrome webdriver instance.

        Returns
        -------
        webdriver
            Instance of the configured Chrome webdriver.
        """
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

    def go_to(self, url: str) -> None:
        self._driver.get(url)

    def enter_text(self, element_content: str, text: str) -> None:
        self._wait_until_loaded(
            EC.visibility_of_element_located((By.ID, element_content))
        )
        element = self._get_element(By.ID, element_content)
        element.send_keys(text)

    def click_element(self, element_content: str) -> None:
        self._wait_until_loaded(
            EC.element_to_be_clickable((By.ID, element_content))
        )
        element = self._get_element(By.ID, element_content)
        element.click()

    def _wait_until_loaded(self, condition: Any) -> None:
        try:
            WebDriverWait(self._driver, self.timeout).until(condition)
        except TimeoutException:
            logger.error("Timed out waiting for condition.")

    def _get_element(
        self, element_type, element_content: str
    ) -> webdriver.Chrome:
        return self._driver.find_element(By.ID, element_content)

    def is_logged(self) -> bool:
        try:
            WebDriverWait(self._driver, self.timeout).until(
                EC.presence_of_element_located(
                    (By.ID, "nav-notifications-label")
                )
            )
            return True
        except TimeoutException:
            return False

    def is_at_homepage(self) -> bool:
        """Check if the ChromeDriver is at the homepage."""
        try:
            WebDriverWait(self._driver, self.timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "[data-test='announcements']")
                )
            )
            return True
        except TimeoutException:
            return False

    def get_page_source(self):
        """Get the page source of the current webpage."""
        return self._driver.page_source


class DriverManager:
    def __init__(self, driver: ChromeDriver):
        self.driver = driver
