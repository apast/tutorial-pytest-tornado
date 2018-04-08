import pytest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions


@pytest.fixture
def browser_firefox():
    options = FirefoxOptions()
    options.set_headless(headless=True)
    return webdriver.Firefox(firefox_options=options)


@pytest.fixture
def browser_chrome():
    options = ChromeOptions()
    options.set_headless(headless=True)
    return webdriver.Chrome(chrome_options=options)


@pytest.fixture(scope="session")
def browser(browser_firefox):
    b = browser_firefox
    yield b
    b.quit()
