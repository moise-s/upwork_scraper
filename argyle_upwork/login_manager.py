"""A module for handling login."""

from argyle_upwork.driver import ChromeDriver, DriverManager
from argyle_upwork.logger import logger


class LoginHandler(DriverManager):
    """A class for handling the login process."""

    def __init__(self, driver: ChromeDriver):
        """Initialize the LoginHandler with Chromedriver."""
        super().__init__(driver)

        # get this variables in a safer way
        self.portal_link: str = (
            "https://www.upwork.com/ab/account-security/login"
        )
        self.username: str = "recruitment+scanners+task@argyle.com"
        self.password: str = "ArgyleAwesome!@"
        self.secret_answer: str = "Jimmy"

    def login(self):
        """Perform the login process."""
        self.driver.go_to_url(self.portal_link)

        logger.info("Login page loaded successfully.")
        self._enter_username()

        logger.info("Password page loaded successfully.")
        self._enter_password()

        if not self._is_logged():
            logger.info("Secret answer page loaded successfully.")
            self._enter_secret_answer()

    def _enter_username(self):
        """Enter the username during the login process."""
        self.driver.enter_text_when_loaded("login_username", self.username)
        self.driver.click_element("login_password_continue")

    def _enter_password(self):
        """Enter the password during the login process."""
        self.driver.enter_text_when_loaded("login_password", self.password)
        self.driver.click_element("login_control_continue")

    def _enter_secret_answer(self):
        """Enter the secret answer during the login process if needed."""
        self.driver.enter_text_when_loaded("login_answer", self.secret_answer)
        self.driver.click_element("login_control_continue")

    def _is_logged(self):
        """Check if the user is logged in."""
        return self.driver.is_logged()
