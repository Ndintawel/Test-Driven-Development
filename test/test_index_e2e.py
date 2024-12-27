import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import time
import requests
from selenium.webdriver.edge.options import Options

@pytest.fixture(scope="module")
def flask_app():
    """Start the Flask app as a subprocess before running tests."""
    flask_process = subprocess.Popen(
        ["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    url = 'http://127.0.0.1:5000'
    max_wait_time = 10  # Max time to wait for the Flask app
    start_time = time.time()

    while time.time() - start_time < max_wait_time:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            time.sleep(0.2)  # Check every 200ms

    yield
    flask_process.terminate()

@pytest.fixture(scope="module")
def browser():
    """Set up the Edge WebDriver in headless mode."""
    edge_service = Service(r'C:\Users\ddago\Downloads\edgedriver_win64\msedgedriver.exe')
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Edge(service=edge_service, options=options)
    yield driver
    driver.quit()

def _find(browser, data_test_id):
    """Helper function to find elements by data-test-id."""
    return browser.find_element(By.CSS_SELECTOR, f'[data-test-id="{data_test_id}"]')

def test_browser_title_contains_app_name(flask_app, browser):
    """Test that the browser title contains the app name."""
    browser.get('http://127.0.0.1:5000')
    assert 'Named Entity Finder' in browser.title

def test_page_heading_is_named_entity_finder(browser):
    """Test that the page heading contains 'Named Entity Finder'."""
    browser.get('http://127.0.0.1:5000')
    heading = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-test-id="heading"]'))
    )
    assert heading.text == 'Named Entity Finder'

def test_page_has_input_for_text(browser):
    """Test that the page has an input element for text."""
    browser.get('http://127.0.0.1:5000')
    input_element = _find(browser, 'input-text')
    assert input_element is not None

def test_page_has_button_for_submitting_text(browser):
    """Test that the page has a button for submitting text."""
    browser.get('http://127.0.0.1:5000')
    submit_button = _find(browser, 'find-button')
    assert submit_button is not None

def test_page_has_ner_table(browser):
    """Test that the page displays a table after submission."""
    browser.get('http://127.0.0.1:5000')
    input_element = _find(browser, 'input-text')
    submit_button = _find(browser, 'find-button')

    # Simulate user input and submission
    input_element.send_keys('Mexico and America share a border')
    submit_button.click()

    # Wait for the table to appear with a shorter timeout
    table = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-test-id="ner-table"]'))
    )
    assert table is not None
