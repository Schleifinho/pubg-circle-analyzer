import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helper.my_logger import logger
import os


def extract_player_names(urls, output_file):
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # Run Firefox in headless mode (optional)
    options.accept_insecure_certs = True  # Accept insecure certificates
    driver_path = os.path.abspath("./helper/geckodriver.exe")
    firefox_path = "C:/Program Files/Mozilla Firefox/firefox.exe"
    options.binary_location = firefox_path

    service = Service(driver_path, log_path="/dev/null")
    driver = webdriver.Firefox(options=options, service=service)

    # empty file
    with open(output_file, "w") as file:
        file.truncate(0)

    #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    for url in urls:
        logger.info(url)
        driver.get(url)


        # wait until table is loaded
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        # Get the full rendered HTML content
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        class_pattern = re.compile(r'\bAdvancedTable_bigCell.*\b')
        table_cells = soup.find_all("td", attrs={"class": class_pattern})

        with open(output_file, "a") as file:
            for t in table_cells:
                player_name_spans = t.find_all("span")
                # Write each line of content to the file
                for player_name_span in player_name_spans:
                    file.write(player_name_span.text + "\n")

    driver.close()

