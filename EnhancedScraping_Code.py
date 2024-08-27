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
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

def create_driver():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://find-and-update.company-information.service.gov.uk/")
    return driver

def scrape_company_details(company_id):
    try:
        driver = create_driver()
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="site-search-text"]'))
        )
        search_bar.clear()
        search_bar.send_keys(company_id)
        search_bar.send_keys(Keys.RETURN)

        try:
            company_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="results"]/li/h3/a'))
            )
            company_link.click()
        except:
            print(f"No company found for ID {company_id}")
            driver.quit()
            return None

        try:
            overdue_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content-container"]/div[2]/div/div[3]/dl/div/h2'))
            )
            if 'Annual statement overdue' not in overdue_element.text:
                print(f"Company {company_id} does not have an overdue annual statement.")
                driver.quit()
                return None
        except:
            print(f"Company {company_id} does not have an overdue annual statement.")
            driver.quit()
            return None

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        company_name = soup.select_one('h1.heading-xlarge').text.strip()
        company_number = soup.select_one('#company-number').text.strip()
        correspondence_address = soup.select_one('#content-container div.govuk-tabs__panel dl dd').text.strip()
        company_status = soup.select_one('#company-status').text.strip()
        company_type = soup.select_one('#company-type').text.strip()
        overdue_date = soup.select_one('#content-container > div.govuk-tabs > div > div:nth-child(4) > dl > p').text.strip()
        registration_date = soup.select_one('#company-creation-date').text.strip() if soup.select_one('#company-creation-date') else 'N/A'
        overseas_entity_address = soup.select_one('#content-container div.govuk-tabs__panel dd').text.strip() if soup.select_one('#content-container div.govuk-tabs__panel dd') else 'N/A'
        incorporated_in = soup.select_one('#incorporated_in').text.strip() if soup.select_one('#incorporated_in') else 'N/A'
        legal_form = soup.select_one('#legal_form').text.strip() if soup.select_one('#legal_form') else 'N/A'
        governing_law = soup.select_one('#governing_law').text.strip() if soup.select_one('#governing_law') else 'N/A'

        return {
            'Company Name': company_name,
            'Company Number': company_number,
            'Correspondence address': correspondence_address,
            'Company Status': company_status,
            'Company Type': company_type,
            'Overseas Entity Address': overseas_entity_address,
            'Annual Statement Overdue': overdue_date,
            'Incorporated In': incorporated_in,
            'Legal Form': legal_form,
            'Governing Law': governing_law,
            'Registration Date': registration_date
        }
    except Exception as e:
        print(f"Error scraping company ID {company_id}: {e}")
        return None

def main():
    data = []
    start_id = "OE030711"
    prefix = start_id[:2]
    numeric_part = int(start_id[2:])

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_company_id = {executor.submit(scrape_company_details, f"{prefix}{numeric_part + i:06d}"): i for i in range(0,1000)}
        for future in as_completed(future_to_company_id):
            company_id = future_to_company_id[future]
            try:
                details = future.result()
                if details:
                    data.append(details)
            except Exception as e:
                print(f"Exception for company ID {company_id}: {e}")

    df = pd.DataFrame(data)
    excel_filename = 'Data_5k_two.xlsx'
    df.to_excel(excel_filename, index=False)

if __name__ == "__main__":
    main()
