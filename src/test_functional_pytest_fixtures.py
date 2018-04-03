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


@pytest.fixture
def browser(browser_firefox):
    b = browser_firefox
    yield b
    b.quit()


def test_title_should_be_for_converter(browser):
    browser.get("http://localhost:8000")
    assert "dimdim converter" in browser.title


def test_content_should_not_be_empty(browser):
    browser.get("http://localhost:8000")
    assert len(browser.find_element_by_tag_name("body").text) > 0
