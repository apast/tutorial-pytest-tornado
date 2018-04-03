import unittest

from selenium import webdriver


class ConverterPageTestCase(unittest.TestCase):
  def setUp(self):
    self.browser = webdriver.Firefox()

  def tearDown(self):
    self.browser.quit()

  def test_title_should_be_for_converter(self):
    self.browser.get("http://localhost:8000")
    self.assertIn("dimdim converter", self.browser.title)

  def test_content_should_not_be_empty(self):
    response = self.browser.get("http://localhost:8000")
    self.assertGreater(len(self.browser.find_element_by_tag_name("body").text), 0)
