import cli
import selenium
from plib import Path
from retry import retry
from selenium.common.exceptions import (InvalidCookieDomainException,
                                        NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys


class Browser(selenium.webdriver.Chrome):
    def __init__(
        self,
        headless=True,
        cookies_path=None,
        base_url=None,
        logging=False,
        experimental_options={},
    ):
        self.cookies_path = Path(cookies_path) if cookies_path else None
        self.base_url = base_url
        if self.base_url and not self.base_url.endswith("/"):
            self.base_url = self.base_url + "/"

        chrome_options = selenium.webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        if headless:
            chrome_options.add_argument("headless")
        for name, value in experimental_options.items():
            chrome_options.add_experimental_option(name, value)

        path = cli.get("which chromium") + ".chromedriver"
        if logging:
            capabilities = selenium.webdriver.DesiredCapabilities.CHROME
            capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        else:
            capabilities = None

        super().__init__(
            path, options=chrome_options, desired_capabilities=capabilities
        )

        if self.base_url:
            self.get(base_url)
        if self.cookies_path:
            for cookie in self.cookies_path.content:
                try:
                    self.add_cookie(cookie)
                except InvalidCookieDomainException:
                    pass
        if self.base_url:
            self.get(base_url)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cookies_path:
            if self.base_url:
                self.get(self.base_url)

            self.cookies_path.content = self.get_cookies()

        super().__exit__()

    @property
    def domain(self):
        return self.current_url.replace("https://", "").split("/")[0]

    @property
    def domain_name(self):
        return self.domain.replace(".", "")

    def click_by_name(self, name):
        self.click_by_condition(lambda button: button.text == name)

    @retry((StaleElementReferenceException, StopIteration), delay=1)
    def click_by_condition(self, condition):
        for button in self.find_elements_by_tag_name("button"):
            if condition(button):
                button.click()

    def click_link_by_name(self, name):
        buttons = (b for b in self.find_elements_by_tag_name("a") if b.text == name)
        next(buttons).click()

    def is_present(self, id):
        try:
            super().find_element_by_id(id)
        except NoSuchElementException:
            present = False
        else:
            present = True
        return present

    @retry(NoSuchElementException, tries=10, delay=1)
    def find_element_by_id(self, id_):
        return super().find_element_by_id(id_)

    def get(self, url):
        if not url.startswith("http"):
            url = self.base_url + url
        return super().get(url)

    def fill_in(self, items, add_enter=True, ignored_exceptions=()):
        for id_, value in items.items():
            try:
                self.fill_in_field(id_, value, add_enter=add_enter)
            except ignored_exceptions:
                pass

    def fill_in_field(self, id_, value, add_enter):
        field = self.find_element_by_id(id_)
        if value is None:
            field.click()
        if not field.get_property("value"):  # don't fill in twice
            keys = ((value, Keys.ENTER) if add_enter else value,)
            field.send_keys(*keys)
