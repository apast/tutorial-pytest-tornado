import pytest


@pytest.fixture
def home_pageobject(browser):
    home = HomePageObject(browser)
    home.get()
    return home


class HomePageObject():

    def __init__(self, browser):
        self.browser = browser

    def get(self):
        self.browser.get("http://localhost:8000")

    def get_from_currency_value(self):
        return self.browser.find_element_by_css_selector("select.from_currency").get_attribute("value")

    def get_to_currency_value(self):
        return self.browser.find_element_by_css_selector("select.to_currency").get_attribute("value")

    def get_from_amount_value(self):
        return self.browser.find_element_by_name("from_amount").get_attribute("value")

    def get_to_amount_value(self):
        return self.browser.find_element_by_css_selector(".to_amount").text

    def set_to_currency_value(self, curr):
        self.browser.find_element_by_css_selector("select.to_currency").set_attribute("value", curr)

    def set_from_amount_value(self, value):
        self.browser.find_element_by_name("from_amount").set_attribute("value", value)

    def submit_form(self):
        self.browser.find_element_by_id("convert_form").submit()


def test_title_should_be_for_converter(browser):
    browser.get("http://localhost:8000")
    assert "dimdim converter" in browser.title


def test_content_should_not_be_empty(browser):
    browser.get("http://localhost:8000")
    assert len(browser.find_element_by_tag_name("body").text) > 0


def test_initial_fields_setup_should_be_one_usd_to_brl(home_pageobject):
    assert "USD" == home_pageobject.get_from_currency_value()
    assert "BRL" == home_pageobject.get_to_currency_value()
    assert "1" == home_pageobject.get_from_amount_value()


def test_one_usd_to_brl_should_return_unitary_conversion(home_pageobject):
    assert "1" == home_pageobject.get_to_amount_value()


def test_two_usd_should_return_double_value_in_brl(home_pageobject):
    home_pageobject.set_from_amount_value("2")
    home_pageobject.submit()

    assert "2" == home_pageobject.get_to_amount_value()
