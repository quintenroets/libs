from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time

from libs.cli import Cli
from spathlib import Path


class Browser(Chrome):
    def load_cookies(self):
        cookies = self.cookies_path.load()
        for cookie in cookies:
            self.add_cookie(cookie)

    def __init__(self, headless=True, cookies_path=None, base_url=None, logging=False):
        self.cookies_path = Path(cookies_path) if cookies_path else None
        self.base_url = base_url
        if self.base_url and not self.base_url.endswith("/"):
            self.base_url = self.base_url + "/"

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        if headless:
            chrome_options.add_argument("headless")

        path = Cli.get("which chromium") + ".chromedriver"
        if logging:
            capabilities = DesiredCapabilities.CHROME
            capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        else:
            capabilities = None

        super().__init__(path, options=chrome_options, desired_capabilities=capabilities)

        if self.base_url:
            self.get(base_url)
        if self.cookies_path:
            self.load_cookies()
        if self.base_url:
            self.get(base_url)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cookies_path:
            if self.base_url:
                self.get(self.base_url)

            cookies = self.get_cookies()
            self.cookies_path.save(cookies)

        self.close()
        self.quit()

    def click_by_name(self, name):
        self.click_by_condition(lambda button: button.text == name)

    def click_by_condition(self, condition):
        succes = False
        while not succes:
            try:
                buttons = (b for b in self.find_elements_by_tag_name("button") if condition(b))
                next(buttons).click()
                succes = True
            except (StaleElementReferenceException, StopIteration):
                time.sleep(1)

    def click_link_by_name(self, name):
        buttons = (b for b in self.find_elements_by_tag_name("a") if b.text == name)
        next(buttons).click()

    def get(self, url):
        if not url.startswith("http"):
            url = self.base_url + url
        return super().get(url)
