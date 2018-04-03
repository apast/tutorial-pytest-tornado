from selenium import webdriver


def test_title_should_be_for_converter():
  browser = webdriver.Firefox()
  browser.get("http://localhost:8000")
  assert "dimdim converter" in browser.title
  browser.quit()

def test_content_should_not_be_empty():
  browser = webdriver.Firefox()
  browser.get("http://localhost:8000")
  assert len(browser.find_element_by_tag_name("body").text) > 0
  browser.quit()
