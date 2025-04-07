"""Main module for the Argyle Upwork project."""

from dotenv import load_dotenv

from upwork_scraper.driver import ChromeDriver
from upwork_scraper.homepage_scanner import HomepageScanner
from upwork_scraper.logger import logger
from upwork_scraper.login_manager import LoginHandler
from upwork_scraper.profile_scanner import ProfileScanner


def handler():
    """Run the main handler."""
    load_dotenv()
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
