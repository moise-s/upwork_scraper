"""Main module for the Argyle Upwork project."""

import asyncio

from dotenv import load_dotenv

from argyle_upwork.driver import ChromeDriver
from argyle_upwork.homepage_scanner import HomepageScanner
from argyle_upwork.logger import logger
from argyle_upwork.login_manager import LoginHandler
from argyle_upwork.profile_scanner import ProfileScanner


async def handler():
    load_dotenv()

    chrome_driver = ChromeDriver(headless=False)
    login_manager = LoginHandler(chrome_driver)
    login_manager.login()
    logger.info("Login successful.")

    homepage_scanner = HomepageScanner(chrome_driver)
    profile_scanner = ProfileScanner(chrome_driver)

    homepage_task = asyncio.create_task(homepage_scanner.scan_homepage())
    profile_task = asyncio.create_task(profile_scanner.scan_profile())

    await asyncio.gather(profile_task, homepage_task)
    logger.info("Homepage and Profile scanned successfully.")

asyncio.run(handler())
