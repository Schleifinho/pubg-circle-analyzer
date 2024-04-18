import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.pubg_api_config import HEADER_NO_AUTH


def extract_player_names(urls, output_file):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    for url in urls:
        driver.get(url)

        # wait until table is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        # Get the full rendered HTML content
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        class_pattern = re.compile(r'\bAdvancedTable_bigCell.*\b')
        table_cells = soup.find_all("td", attrs={"class": class_pattern})

        with open(output_file, "w") as file:
            for t in table_cells:
                player_name_spans = t.find_all("span")
                # Write each line of content to the file
                for player_name_span in player_name_spans:
                    file.write(player_name_span.text + "\n")

