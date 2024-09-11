from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed



chrome_options = Options()
chrome_options.add_argument("__headless")

chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

def create_driver():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://find-and-update.company-information.service.gov.uk/")
    return driver

