from driver import ChromeDriver
from logger import logger
from driver import DriverManager


class LoginManager(DriverManager):
    def __init__(self, driver: ChromeDriver):
        super().__init__(driver)
        self.portal_link: str = "https://www.upwork.com/ab/account-security/login"
        self.username = "recruitment+scanners+task@argyle.com"
        self.password = "ArgyleAwesome!@"
        self.secret_answer = "Jimmy"

    def login(self):
        self.driver.go_to(self.portal_link)
        logger.info("Login page loaded successfully.")
        self._enter_username()
        self._enter_password()
        self._enter_secret_answer()

    def _enter_username(self):
        self.driver.enter_text("login_username", self.username)
        self.driver.click_element("login_password_continue")

    def _enter_password(self):
        self.driver.enter_text("login_password", self.password)
        self.driver.click_element("login_control_continue")

    def _enter_secret_answer(self):
        self.driver.enter_text("login_answer", self.secret_answer)
        self.driver.click_element("login_control_continue")
