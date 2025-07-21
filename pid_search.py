from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

# Input for PIDs
input_string = input("Enter comma-separated values: ")
string_list = input_string.split(',')

# List of PIDs to search
pids = string_list  # Replace with your list

all_data = []
headers = None

for pid in pids:
    # Open driver
    driver = webdriver.Chrome()
    driver.get("https://gis.dot.state.oh.us/tims_classic/projects")
    wait = WebDriverWait(driver, 15)

    time.sleep(7)   # Give extra time to load dropdown
    # Click the PID dropdown and enter PID
    dropdown_shell = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.project-select .selectize-input")))
    dropdown_shell.click()

    actions = ActionChains(driver)
    actions.send_keys(Keys.BACKSPACE).send_keys(pid).perform()
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(3)  # Wait for results to load

    # Click the result row to activate
    result_row = wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id='results-table']//tbody/tr")))
    result_row.click()
    time.sleep(1)  # Small pause

    # Parse page for table data
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    if headers is None:
        header_cells = soup.select("#results-table thead tr th")[1:]
        headers = [th.get_text(strip=True) for th in header_cells]

    rows = soup.select("#results-table tbody tr.odd.active, #results-table tbody tr.even.active")
    for row in rows: # Collect and append data
        cols = row.find_all("td")[1:]  # Skip first column with search icon
        all_data.append([td.get_text(strip=True) for td in cols])

    driver.quit()

# Convert to dataframe
df = pd.DataFrame(all_data, columns=headers)
print(df)
# Export to excel file
df.to_excel("project_info.xlsx", index=False)
