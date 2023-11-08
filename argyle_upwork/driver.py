from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ChromeDriver:
    """
    A class to manage the Selenium webdriver for Google Chrome.
    """

    def __init__(self, headless: bool = True):
        """
        Initializes the Driver class with specified parameters.

        Parameters
        ----------
        headless : bool, optional
            Starts the browser in headless mode if True, by default True.
        """
        self.headless = headless
        self.driver = self._create_driver()

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
                # "download.default_directory": self.dir_download,
                # "download.directory_upgrade": True,
            },
        )
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        )

        if self.headless:
            options.add_argument("--headless")

        return webdriver.Chrome(
            options=options, service=Service(ChromeDriverManager().install())
        )

    def get_driver(self) -> webdriver.Chrome:
        """
        Returns the configured Chrome webdriver instance.

        Returns
        -------
        webdriver
            Instance of the configured Chrome webdriver.
        """
        return self.driver
