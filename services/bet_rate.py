from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from configs.nba_team import NBA_FULL_NAME
from configs.params import (
    START_YEAR, 
    END_YEAR,
    HEADERS
)
from utils.utils import (
    write_csv,
    write_log,
    get_year,
    is_ready
)
from utils import logging
log = logging.Logger()

# -- set configs params
url = 'https://nflpickwatch.com/nba/picks/ou/combined/2023-05-09'
URL = 'https://nflpickwatch.com/nba/picks/ou/combined/{date}'

def login(driver):
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "btn d-none d-lg-inline-block text-white pr-0 pl-lg-2 btn-white")))
    driver.find_element(By.CLASS_NAME, "btn d-none d-lg-inline-block text-white pr-0 pl-lg-2 btn-white").click()
    # driver.find_element_by_id("PASSOFLOGIN").sendKeys("Trancalvin8899@gmail.com")
    # driver.find_element_by_id("").sendKeys("thuongbella2013")
    # driver.find_element_by_id("login button").click()

def crawler():
    # -- set configs selenium
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 10).until(is_ready)
    login(driver)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # WebDriverWait(driver, 10).until(is_ready)

    # html_content = driver.page_source
    # soup = BeautifulSoup(html_content, 'html.parser')

def run():
    crawler()