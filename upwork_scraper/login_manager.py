"""A module for handling login."""

from retry import retry

from upwork_scraper.driver import ChromeDriver, DriverManager
from upwork_scraper.logger import logger


class LoginHandler(DriverManager):
    """A class for handling the login process."""

    def __init__(self, driver: ChromeDriver):
        """Initialize the LoginHandler with Chromedriver."""
        super().__init__(driver)

    @retry(exceptions=Exception, tries=3, delay=2, backoff=2)
    def login(self) -> None:
        """Perform the login process."""
        self.driver.go_to_url(self.driver.login_url)

        logger.info("Login page loaded successfully.")
        self._enter_username()

        logger.info("Password page loaded successfully.")
        self._enter_password()

        if not self._is_logged():
            logger.info("Secret answer page loaded successfully.")
            self._enter_secret_answer()

    def _enter_username(self) -> None:
        """Enter the username during the login process."""
        self.driver.enter_text_when_loaded("login_username", self.username)
        self.driver.click_element("login_password_continue")

    def _enter_password(self) -> None:
        """Enter the password during the login process."""
        self.driver.enter_text_when_loaded("login_password", self.password)
        self.driver.click_element("login_control_continue")

    def _enter_secret_answer(self) -> None:
        """Enter the secret answer during the login process if needed."""
        self.driver.enter_text_when_loaded("login_answer", self.secret_answer)
        self.driver.click_element("login_control_continue")

    def _is_logged(self) -> bool:
        """Check if the user is logged in."""
        return self.driver.is_logged()
