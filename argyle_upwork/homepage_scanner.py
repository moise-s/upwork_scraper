"""A module for scanning the Upwork homepage for job sections."""

import asyncio
import json
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup

from argyle_upwork.driver import ChromeDriver, DriverManager
from argyle_upwork.logger import logger
from argyle_upwork.models.job import JobSection


class HomepageScanner(DriverManager):
    """A class for scanning the Upwork homepage for job sections."""

    def __init__(self, driver: ChromeDriver):
        """Initialize the HomepageScanner with Chromedriver."""
        super().__init__(driver)
        self.job_sections: list[dict] = []
        self.datetime_now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def scan_homepage(self) -> None:
        """Scan the Upwork homepage for job sections."""
        if not await self._is_at_homepage():
            await self.driver.go_to_url(self.driver.homepage_url)
        logger.info("Homepage loaded successfully.")

        await self._scan_page_source()
        logger.info("Page source extracted successfully.")

        await self._scan_job_sections_from_page_source()
        logger.info("Job sections extracted successfully.")

        await self._scan_job_section_data()
        logger.info("Job sections parsed successfully.")

        await self._store_job_sections_locally()
        logger.info("Job sections stored successfully.")

    async def _is_at_homepage(self) -> bool:
        """Check if the driver is at the homepage."""
        return self.driver.is_at_homepage()

    async def _scan_page_source(self) -> None:
        """Scan the page source of the homepage."""
        self.page_source = self.driver.get_page_source()

    async def _scan_job_sections_from_page_source(self) -> None:
        """Scan job sections from the page source."""
        soup = BeautifulSoup(self.page_source, "html.parser")
        self.job_sections_source_code = soup.find_all(
            "section",
            class_="up-card-section up-card-list-section up-card-hover",
        )

    async def _get_text_or_none(self, element) -> str:
        """Return the text if it exists, else return None."""
        return element.text.strip() if element else None

    async def _scan_job_section_data(self) -> None:
        """Scan data from the job sections."""
        for section in self.job_sections_source_code:
            # fmt: off
            data: dict = {}
            data["title"] = await self._get_text_or_none(section.find("a", class_="up-n-link"))
            data["description"] = await self._get_text_or_none(section.find("span", {"data-test": "job-description-text"}))
            data["proposals"] = await self._get_text_or_none(section.find("strong", {"data-test": "proposals"}))
            data["posted_on"] = await self._get_text_or_none(section.find("span", {"data-test": "posted-on"}))
            data["country"] = await self._get_text_or_none(section.find("small", {"data-test": "client-country"}))
            data["budget"] = await self._get_text_or_none(section.find("span", {"data-test": "budget"}))
            data["job_type"] = await self._get_text_or_none(section.find("strong", {"data-test": "job-type"}))
            data["duration"] = await self._get_text_or_none(section.find("span", {"data-test": "duration"}))
            data["experience"] = await self._get_text_or_none(section.find("span", {"data-test": "contractor-tier"}))
            data["client_spendings"] = await self._get_text_or_none(section.find("span", {"data-test": "formatted-amount"}))
            data["skills"] = await asyncio.to_thread(lambda: [skill.text for skill in section.find_all("a", class_="up-skill-badge text-muted")])
            data["payment_verified"] = bool(section.find("div", class_="up-icon text-complimentary"))
            data["link"] = section.find("a", class_="up-n-link").get("href")
            # fmt: on
            job_section = JobSection(**data)
            self.job_sections.append(job_section.dict())

    async def _store_job_sections_locally(self) -> None:
        """Store the job sections locally as a JSON file."""
        file_path = Path("data", f"homepage-{self.datetime_now}.json")

        async def write_to_file():
            with file_path.open("w") as file:
                json.dump(self.job_sections, file, indent=4)

        await asyncio.ensure_future(write_to_file())
