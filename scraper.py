from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import re
import io
from pdfminer.high_level import extract_text
from typing import List

def get_all_links_pdfs(query: str, company_site: str) -> List[str]:
    """
    Gathers, saves and returns list of links for given company_site url, using the provided query.
    """
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
    scraped_links = []
    for result in soup.find_all("a", {"href": True}):
        if result["href"] and result["href"].startswith(f'https://{company_site}'):
            with open('links_to_pdfs.txt', 'a') as f:
                f.write(result["href"] + '\n')
            scraped_links.append(result["href"])
    
    # return list of scraped list without duplicates
    return list(set(scraped_links))

def save_scrf_file(pdf_file_url: str, company_code: str, company_name: str, destination_dir: str = './'):
    """
    Saves a PDF file into a specified directory with the appropriate name of <[year]_SFCR_[company code]_[company name].pdf>.
    Ignores the pdf files which are not related to the desired insurance company.
    Extracts year information from the pdf_file_url. 
    """
    # get pdf content from the given url
    response = requests.get(pdf_file_url)

    # extract infromation about year (`unkown` if not found)
    with io.BytesIO(response.content) as stream:
        pdf_text = extract_text(stream, page_numbers=[0])

    year_info = re.search(re.compile(r'\b20\d{2}\b'), pdf_text)
    year = year_info.group() if year_info is not None else 'unkown'
    
    # define the name of the pdf file according to the specified format
    filename = f"{year}_SFCR_{company_code}_{company_name}.pdf"


    if response.status_code == 200:
        with open(destination_dir + filename, 'wb') as file:
            file.write(response.content)
    else:
        print("Failed to download the file.")
    

def main():
    df = pd.read_csv('data/zaklady.csv', sep=';')

    years = [2018, 2019, 2020, 2021, 2022]
    for _, row in df.iterrows():
        company_site = row['LINK DO STRONY ZAKŁADU']
        company_code = row['KOD LEI ZAKŁADU']
        company_name = row['NAZWA ZAKŁADU']
        for year in years:
            print(company_site, year)
            query = f'Sprawozdanie o wypłacalności i kondycji finansowej OR Solvency and financial condition report OR Sprawozdanie na temat wypłacalności i kondycji finansowej OR SFCR site:{company_site} filetype:pdf {company_name} {year}'
            try:
                pdf_urls = get_all_links_pdfs(query, company_site)
                for pdf_url in pdf_urls:
                    save_scrf_file(pdf_url, company_code, company_name,
                                    destination_dir='./data/sfcr/')
            except:
                time.sleep(10)
            

if __name__ == '__main__':
    main()
