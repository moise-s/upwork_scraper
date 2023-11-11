"""Main module for the Argyle Upwork project."""

from argyle_upwork.driver import ChromeDriver
from argyle_upwork.homepage_scanner import HomepageScanner
from argyle_upwork.logger import logger
from argyle_upwork.login_manager import LoginHandler
from argyle_upwork.profile_scanner import ProfileScanner


def handler():
    """Run the main handler."""
    chrome_driver = ChromeDriver()

    login_manager = LoginHandler(chrome_driver)
    login_manager.login()
    logger.info("Login successful.")

    homepage_scanner = HomepageScanner(chrome_driver)
    homepage_scanner.scan_homepage()
    logger.info("Homepage scanned successfully.")

    profile_scanner = ProfileScanner(chrome_driver)
    profile_scanner.scan_profile()
    logger.info("Profile scanned successfully.")


handler()
