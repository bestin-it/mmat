from playwright.sync_api import sync_playwright

class PlaywrightDriver:
    """
    Manages browser interactions using Playwright.
    """
    def __init__(self, config):
        """
        Initializes the PlaywrightDriver.

        Args:
            config (dict): Configuration for the Playwright driver.
        """
        self.config = config
        self.browser = None
        self.page = None
        print("[PlaywrightDriver] Initialized.")

    def launch_browser(self, browser_type="chromium", headless=True):
        """
        Launches a browser instance.

        Args:
            browser_type (str): Type of browser to launch (e.g., 'chromium', 'firefox', 'webkit').
            headless (bool): Whether to run the browser in headless mode.
        """
        print(f"[PlaywrightDriver] Launching {browser_type} browser (headless={headless}).")
        try:
            p = sync_playwright().start()
            if browser_type == "chromium":
                self.browser = p.chromium.launch(headless=headless)
            elif browser_type == "firefox":
                self.browser = p.firefox.launch(headless=headless)
            elif browser_type == "webkit":
                self.browser = p.webkit.launch(headless=headless)
            else:
                print(f"[PlaywrightDriver] Warning: Unsupported browser type '{browser_type}'. Launching chromium.")
                self.browser = p.chromium.launch(headless=headless)

            self.page = self.browser.new_page()
            print("[PlaywrightDriver] Browser launched and new page created.")
        except Exception as e:
            print(f"[PlaywrightDriver] Error launching browser: {e}")
            self.browser = None
            self.page = None

    def navigate(self, url):
        """
        Navigates the current page to a URL.

        Args:
            url (str): The URL to navigate to.
        """
        if self.page:
            print(f"[PlaywrightDriver] Navigating to {url}")
            try:
                self.page.goto(url)
                print(f"[PlaywrightDriver] Successfully navigated to {url}")
            except Exception as e:
                print(f"[PlaywrightDriver] Error navigating to {url}: {e}")
        else:
            print("[PlaywrightDriver] Error: No page available. Launch browser first.")

    def click(self, selector):
        """
        Clicks an element matching the selector.

        Args:
            selector (str): CSS selector for the element.
        """
        if self.page:
            print(f"[PlaywrightDriver] Clicking element with selector: {selector}")
            try:
                self.page.click(selector)
                print(f"[PlaywrightDriver] Successfully clicked element with selector: {selector}")
            except Exception as e:
                print(f"[PlaywrightDriver] Error clicking element with selector {selector}: {e}")
        else:
            print("[PlaywrightDriver] Error: No page available. Launch browser first.")

    def fill(self, selector, value):
        """
        Fills an input field with the given value.

        Args:
            selector (str): CSS selector for the input field.
            value (str): The value to fill.
        """
        if self.page:
            print(f"[PlaywrightDriver] Filling element with selector: {selector}")
            try:
                self.page.fill(selector, value)
                print(f"[PlaywrightDriver] Successfully filled element with selector: {selector}")
            except Exception as e:
                print(f"[PlaywrightDriver] Error filling element with selector {selector}: {e}")
        else:
            print("[PlaywrightDriver] Error: No page available. Launch browser first.")

    def screenshot(self, path):
        """
        Takes a screenshot of the current page.

        Args:
            path (str): Path to save the screenshot.
        """
        if self.page:
            print(f"[PlaywrightDriver] Taking screenshot and saving to {path}")
            try:
                self.page.screenshot(path=path)
                print(f"[PlaywrightDriver] Successfully saved screenshot to {path}")
            except Exception as e:
                print(f"[PlaywrightDriver] Error taking screenshot: {e}")
        else:
            print("[PlaywrightDriver] Error: No page available. Launch browser first.")


    def close_browser(self):
        """
        Closes the browser instance.
        """
        if self.browser:
            print("[PlaywrightDriver] Closing browser.")
            try:
                self.browser.close()
                print("[PlaywrightDriver] Browser closed.")
            except Exception as e:
                print(f"[PlaywrightDriver] Error closing browser: {e}")
            self.browser = None
            self.page = None
        else:
            print("[PlaywrightDriver] No browser instance to close.")

    # Add other methods for browser interaction (e.g., keyboard input, waiting for elements, etc.)
