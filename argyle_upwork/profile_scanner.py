import json
import time
from pathlib import Path
import re
from bs4 import BeautifulSoup

from argyle_upwork.driver import ChromeDriver, DriverManager
from argyle_upwork.logger import logger
from argyle_upwork.models.contact_section import AccountSection
from argyle_upwork.models.location_section import LocationSection
from argyle_upwork.models.profile_section import ProfileSection
from datetime import datetime


class ProfileScanner(DriverManager):
    """A class for scanning the Upwork Profile information."""

    def __init__(self, driver: ChromeDriver):
        """Initialize the ProfileScanner with Chromedriver."""
        super().__init__(driver)
        self.secret_answer: str = "Jimmy"
        self.password: str = "ArgyleAwesome!@"
        self.contact_sections: list[dict] = []
        self.location_sections: list[dict] = []
        self.profile_sections: list[dict] = []
        self.datetime_now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def scan_profile(self):
        """Scan the Upwork Profile page."""
        self._scan_contact_info_page()
        self._scan_profile_page()

    def _scan_profile_page(self):
        """Scan the Upwork Profile page."""
        if not self._is_at_profile_page():
            self.driver.go_to_url(self.driver.profile_page_url)
        logger.info("Profile page loaded successfully.")

        self._scan_page_source()
        logger.info("Page source extracted successfully.")

        self._scan_page_soup_from_source()
        logger.info("Soup object extracted successfully.")

        self._scan_profile_data()
        logger.info("Profile sections parsed successfully.")

        self._store_profile_sections_locally()
        logger.info("Profile sections stored successfully.")

    def _store_profile_sections_locally(self):
        """Store the profile sections locally as a JSON file."""
        file_path = Path("data", f"profile-{self.datetime_now}.json")
        with file_path.open("w") as file:
            json.dump(self.profile_sections, file, indent=4)

    def _get_text_or_none(self, element) -> str:
        """Return the text if it exists, else return None."""
        return element.text.strip() if element else None

    def _scan_profile_data(self):
        """Scan data from the profile page."""
        data: dict = {}
        # fmt: off
        data["title"] = self._get_text_or_none(self.page_soup.find("h2", {'class': ['mb-0', 'h4']}))
        data["hourly_rate"] = self._get_text_or_none(self.page_soup.find("h3", {'class': ['my-6x', 'h5']}))
        data["description"] = self._get_text_or_none(self.page_soup.find("div", class_="air3-line-clamp"))
        data["skills"] = [skill.text for skill in self.page_soup.find_all("span", class_="air3-token")]
        data["employment_history"] = self._extract_employment_history()
        # fmt: on

        profile_section = ProfileSection(**data)
        self.profile_sections.append(profile_section.dict())

    def _extract_employment_history(self):
        """Extract the employment history from the profile page."""
        employment_history_section = self.page_soup.find(
            "h3", text=re.compile(r"\s*Employment history\s*")
        )
        if not employment_history_section:
            return []
        employment_history_list = []
        employment_history_div = (
            employment_history_section.find_previous("div")
            .find_previous("div")
            .find_previous("div")
        )
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

    def _is_at_profile_page(self):
        """Check if the driver is at the profile page."""
        return self.driver.is_at_profile_page()

    def _scan_contact_info_page(self):
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
        self._store_account_sections_locally()
        logger.info("Account sections stored successfully.")

        self._scan_location_info_data()
        logger.info("Location sections parsed successfully.")
        self._store_location_sections_locally()
        logger.info("Location sections stored successfully.")

    def _store_account_sections_locally(self):
        """Store the contact sections locally as a JSON file."""
        file_path = Path("data", f"contact-{self.datetime_now}.json")
        with file_path.open("w") as file:
            json.dump(self.contact_sections, file, indent=4)

    def _store_location_sections_locally(self):
        """Store the location sections locally as a JSON file."""
        file_path = Path("data", f"location-{self.datetime_now}.json")
        with file_path.open("w") as file:
            json.dump(self.location_sections, file, indent=4)

    def _scan_location_info_data(self):
        data: dict = {}
        # fmt: off
        data["adress_street"] = self._get_text_or_none(self.page_soup.find("span", {"data-test": "addressStreet"}))
        data["adress_street_2"] = self._get_text_or_none(self.page_soup.find("span", {"data-test": "addressStreet2"}))
        data["address_city"] = self._get_text_or_none(self.page_soup.find("span", {"data-test": "addressCity"}))
        data["address_state"] = self._get_text_or_none(self.page_soup.find("span", {"data-test": "addressState"}))
        data["address_zip"] = self._get_text_or_none(self.page_soup.find("span", {"data-test": "addressZip"}))
        data["address_country"] = self._get_text_or_none(self.page_soup.find("span", {"data-test": "addressCountry"}))
        data["phone"] = self._get_text_or_none(self.page_soup.find("div", {"data-test": "phone"}))
        # fmt: on
        location_section = LocationSection(**data)
        self.location_sections.append(location_section.dict())

    def _scan_account_info_data(self):
        data: dict = {}
        # fmt: off
        data["user_id"] = self._get_text_or_none(self.page_soup.find("div", {"data-test": "userId"}))
        data["user_name"] = self._get_text_or_none(self.page_soup.find("div", {"data-test": "userName"}))
        data["user_masked_email"] = self._get_text_or_none(self.page_soup.find("div", {"data-test": "userEmail"}))
        # fmt: on
        contact_section = AccountSection(**data)
        self.contact_sections.append(contact_section.dict())

    def _need_to_input_secret_answer(self) -> bool:
        """Check if the page required to input the secret answer."""
        return self.driver.is_element_present("deviceAuth_answer")

    def _enter_secret_answer(self):
        """Enter the secret answer during the login process if needed."""
        self.driver.enter_text_when_loaded(
            "deviceAuth_answer", self.secret_answer
        )
        self.driver.click_element("control_save")

    def _need_to_input_password(self) -> bool:
        """Check if the page required to input the password."""
        return self.driver.is_element_present("reenterPassword")

    def _enter_password(self):
        """Enter the password during the login process."""
        self.driver.enter_text_when_loaded(
            "sensitiveZone_password", self.password
        )
        self.driver.click_element("control_continue")

    def _scan_page_source(self):
        """Scan the page source of the homepage."""
        self.page_source = self.driver.get_page_source()

        # for debugging: save page source in a file
        with open("page_source.txt", "w") as f:
            f.write(self.page_source)

    def _is_at_contact_info_page(self) -> bool:
        """Check if the driver is at the contact info page."""
        return self.driver.is_at_contact_info_page()

    def _scan_page_soup_from_source(self):
        """Scan the page soup from the page source."""
        self.page_soup = BeautifulSoup(self.page_source, "html.parser")
