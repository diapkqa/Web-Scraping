from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get('https://dev.figsflow.com/signin')
driver.maximize_window()

# Login
USER_EMAIL = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="email"]')))
USER_EMAIL.send_keys('dipak@ukpa.co.uk')
time.sleep(2)

USER_PASSWORD = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
USER_PASSWORD.send_keys('d3Vt#1wjhd@4Py1K')

Login_Button = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
Login_Button.click()
time.sleep(10)

# Find all firm elements
firms = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@role="group" and @aria-roledescription="slide"]'))
    )
for firm in firms:
    firm_name = firm.find_element(By.TAG_NAME, 'h3').text
    if firm_name == "Jackson-Ryan":
        firm.click()
        time.sleep(10)
        break


checkbox_buttons = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="flex flex-row flex-wrap gap-2"]/li/label/button'))
)

for button in checkbox_buttons:
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(button)
    ).click()
print("All checkboxes have been clicked.")


radio_button_visible = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@value="201-500 employees"]/preceding-sibling::button'))
)
radio_button_visible.click()
aria_checked = radio_button_visible.get_attribute("aria-checked")
print(f"Radio button selected: {aria_checked}")

time.sleep(1)

Number_Of_Clients= WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//input[@value="201-1000 Clients"]/preceding-sibling::button')))
Number_Of_Clients.click()
aria_checked = radio_button_visible.get_attribute("aria-checked")
time.sleep(1)

Annual_Revenue_Range= WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//input[@value="500K to 1 Million"]/preceding-sibling::button')))
Annual_Revenue_Range.click()
time.sleep(5)

try:

    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
    )
    next_button.click()
    time.sleep(3)
    print("Clicked the Next button successfully.")


except Exception as e:
    print(f"An error occurred: {e}")


try:
    # Wait until the "Step 2" element is present on the page
    step_2_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[text()='Step 2']"))
    )

    # Assert that the element is found
    assert step_2_element is not None
    print("Successfully navigated to Step 2 page.")

except AssertionError:
    print("Failed to navigate to Step 2 page.")

except Exception as e:
    print(f"An error occurred: {e}")


#Step-2: Firm Pricing

Default_VAT= WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="VAT"')))
Default_VAT.clear()
Default_VAT.send_keys('25')
time.sleep(5)


def fill_out_fields(position, standard_rate, premium_rate):
    # Click the Charge_Out_Rate button to open input fields
    charge_out_rate_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="charge-out-rate-button-xpath"]'))
    )
    charge_out_rate_button.click()

    # Fill out the fields
    employee_position = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="chargerate.0.position"]'))
    )
    employee_position.send_keys(position)

    standard_hourly_rate = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="chargerate.0.standardHourlyRate"]'))
    )
    standard_hourly_rate.clear()
    standard_hourly_rate.send_keys(standard_rate)

    premium_hourly_rate = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="chargerate.0.premiumHourlyRate"]'))
    )
    premium_hourly_rate.clear()
    premium_hourly_rate.send_keys(premium_rate)
    charge_out_rate_button.click()


# Fill out all fields
fill_out_fields("Analyst", "75", "105")
fill_out_fields("Associate", "105", "125")
fill_out_fields("Manager", "150", "175")
time.sleep(10)




driver.quit()
