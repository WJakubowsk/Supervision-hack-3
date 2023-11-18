from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

def get_all_links_pdfs(query, site):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    # driver = webdriver.Chrome()

    driver.get("https://www.google.com/")

    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "L2AGLb"))
    )
    accept_button.click()

    search_box = driver.find_element("name", "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    driver.quit()
    for result in soup.find_all("a", {"href": True}):
        if result["href"] and result["href"].startswith(f'https://{site}'):
            with open('links_to_pdfs.txt', 'a') as f:
                f.write(result["href"] + '\n')

def main():

    df = pd.read_csv('data/zaklady.csv', sep=';')

    years = [2018, 2019, 2020, 2021, 2022]
    for _, row in df.iterrows():
        site = row['LINK DO STRONY ZAKŁADU']
        nazwa_zakladu = row['NAZWA ZAKŁADU']
        for year in years:
            print(site, year)
            query = f'Sprawozdanie o wypłacalności i kondycji finansowej OR Solvency and financial condition report OR Sprawozdanie na temat wypłacalności i kondycji finansowej OR SFCR site:{site} filetype:pdf {nazwa_zakladu} {year}'
            try:
                get_all_links_pdfs(query, site)
            except:
                time.sleep(10)

if __name__ == '__main__':
    main()
