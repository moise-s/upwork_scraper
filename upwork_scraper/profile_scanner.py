"""A module for scanning the Upwork profile pages."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

from bs4 import BeautifulSoup, NavigableString, Tag
from retry import retry

from upwork_scraper.driver import ChromeDriver, DriverManager
from upwork_scraper.logger import logger
from upwork_scraper.models.profile import (AccountSection, LocationSection,
                                          Profile, ProfilePage)


class ProfileScanner(DriverManager):
    """A class for scanning the Upwork Profile information."""

    def __init__(self, driver: ChromeDriver):
        """Initialize the ProfileScanner with Chromedriver."""
        super().__init__(driver)
        self.datetime_now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.contact_section: AccountSection
        self.location_section: LocationSection
        self.profile_section: ProfilePage
        self.profile: Profile

    @retry(exceptions=Exception, tries=3, delay=2, backoff=2)
    def scan_profile(self) -> None:
        """Scan the Upwork Profile page."""
        self._scan_contact_info_page()
        self._scan_profile_page()
        self._store_profile_info_locally()

    def _store_profile_info_locally(self) -> None:
        """Store the profile info locally as a json file."""
        self.profile = Profile(
            account_session=self.contact_section,
            location_session=self.location_section,
            profile_page=self.profile_section,
        )

        file_path = Path("data", f"profilepage-{self.datetime_now}.json")
        with file_path.open("w") as file:
            json.dump(self.profile.dict(), file, indent=4)

    def _scan_profile_page(self) -> None:
        """Scan the Upwork Profile page."""
        if not self._is_at_profile_page():
            profile_url = self.driver.get_profile_link("/freelancers/")
            self.driver.go_to_url(profile_url)
        logger.info("Profile page loaded successfully.")

        self._scan_page_source()
        logger.info("Page source extracted successfully.")

        self._scan_page_soup_from_source()
        logger.info("Soup object extracted successfully.")

        self._scan_profile_data()
        logger.info("Profile sections parsed successfully.")

    def _get_text_or_none(self, element) -> str:
        """Return the text if it exists, else return None."""
        return element.text.strip() if element else None

    def _scan_profile_data(self) -> None:
        """Scan data from the profile page."""
        data: dict = {}
        # fmt: off
        data["job_title"] = self._get_text_or_none(self.page_soup.find("h2", {'class': ['mb-0', 'h4']}))
        data["hourly_rate"] = self._get_text_or_none(self.page_soup.find("h3", {'class': ['my-6x', 'h5']}))
        data["description"] = self._get_text_or_none(self.page_soup.find("div", class_="air3-line-clamp"))
        data["skills"] = [skill.text for skill in self.page_soup.find_all("span", class_="air3-token")]
        data["employment_history"] = self._extract_employment_history()
        # fmt: on
        self.profile_section = ProfilePage(**data)

    def _extract_employment_history(self) -> list:
        """Extract the employment history from the profile page."""
        employment_history_section: Optional[
            Union[Tag, NavigableString]
        ] = self.page_soup.find("h3", text=re.compile(r"\s*Employment history\s*"))
        if employment_history_section is None:
            return []
        employment_history_list = []
        if isinstance(employment_history_section, Tag):
            employment_history_div = (
                employment_history_section.find_previous("div")
                .find_previous("div")
                .find_previous("div")
            )
        if isinstance(employment_history_div, Tag):
            employment_sections = employment_history_div.find_all(
                "div", class_="air3-card-section px-0"
            )
            for entry in employment_sections:
                title = self._get_text_or_none(entry.find("h4", class_="my-0"))
                period = self._get_text_or_none(
                    entry.find("div", class_="mt-3x text-light-on-inverse")
                )
                employment_entry = {"title": title, "period": period}
                employment_history_list.append(employment_entry)
        return employment_history_list

    def _is_at_profile_page(self) -> bool:
        """Check if the driver is at the profile page."""
        return self.driver.is_at_profile_page()

    def _scan_contact_info_page(self) -> None:
        """Scan the Upwork Profile Contact sub-page."""
        if not self._is_at_contact_info_page():
            self.driver.go_to_url(self.driver.contact_info_url)

        if self._need_to_input_secret_answer():
            self._enter_secret_answer()
            logger.info("Secret answer page loaded successfully.")

        if self._need_to_input_password():
            self._enter_password()

        logger.info("Contact-info page loaded successfully.")

        self._scan_page_source()
        logger.info("Page source extracted successfully.")

        self._scan_page_soup_from_source()
        logger.info("Soup object extracted successfully.")

        self._scan_account_info_data()
        logger.info("Account sections parsed successfully.")

        self._scan_location_info_data()
        logger.info("Location sections parsed successfully.")

    def _scan_location_info_data(self) -> None:
        data: dict = {}
        # fmt: off
        data["line_1"] = self._get_text_or_none(self.page_soup.find("span", {"data-test": "addressStreet"}))
        data["line_2"] = self._get_text_or_none(self.page_soup.find("span", {"data-test": "addressStreet2"}))
        data["city"] = self._get_text_or_none(self.page_soup.find("span", {"data-test": "addressCity"}))
        data["state"] = self._get_text_or_none(self.page_soup.find("span", {"data-test": "addressState"}))
        data["postal_code"] = self._get_text_or_none(self.page_soup.find("span", {"data-test": "addressZip"}))
        data["country"] = self._get_text_or_none(self.page_soup.find("span", {"data-test": "addressCountry"}))
        data["phone_number"] = self._get_text_or_none(self.page_soup.find("div", {"data-test": "phone"}))
        # fmt: on
        self.location_section = LocationSection(**data)

    def _scan_account_info_data(self) -> None:
        data: dict = {}
        # fmt: off
        data["id"] = self._get_text_or_none(self.page_soup.find("div", {"data-test": "userId"}))
        data["full_name"] = self._get_text_or_none(self.page_soup.find("div", {"data-test": "userName"}))
        data["masked_email"] = self._get_text_or_none(self.page_soup.find("div", {"data-test": "userEmail"}))
        # fmt: on
        self.contact_section = AccountSection(**data)

    def _need_to_input_secret_answer(self) -> bool:
        """Check if the page required to input the secret answer."""
        return self.driver.is_element_present("deviceAuth_answer")

    def _enter_secret_answer(self) -> None:
        """Enter the secret answer during the login process if needed."""
        self.driver.enter_text_when_loaded("deviceAuth_answer", self.secret_answer)
        self.driver.click_element("control_save")

    def _need_to_input_password(self) -> bool:
        """Check if the page required to input the password."""
        return self.driver.is_element_present("reenterPassword")

    def _enter_password(self) -> None:
        """Enter the password during the login process."""
        self.driver.enter_text_when_loaded("sensitiveZone_password", self.password)
        self.driver.click_element("control_continue")

    def _scan_page_source(self) -> None:
        """Scan the page source of the homepage."""
        self.page_source = self.driver.get_page_source()

    def _is_at_contact_info_page(self) -> bool:
        """Check if the driver is at the contact info page."""
        return self.driver.is_at_contact_info_page()

    def _scan_page_soup_from_source(self) -> None:
        """Scan the page soup from the page source."""
        self.page_soup = BeautifulSoup(self.page_source, "html.parser")
