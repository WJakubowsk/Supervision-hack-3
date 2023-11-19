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
import argparse
from stqdm import stqdm
import os

def get_all_links_pdfs(query: str, company_site: str, verbose=False) -> List[str]:
    """
    Gathers, saves and returns list of links for given company_site url, using the provided query.
    """
    if verbose:
        print(f"Scraping links for {company_site}...")
        driver = webdriver.Chrome()
    else:
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(options=op)

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
            scraped_links.append(result["href"])

    # return list of scraped list without duplicates
    return list(set(scraped_links))

def save_scrf_file(pdf_file_url: str, company_code: str, company_name: str, destination_dir: str = './'):
    """
    Saves a PDF file into a specified directory with the appropriate name of <[year]_SFCR_[company code]_[company name].pdf>.
    Ignores the pdf files which are not related to the desired insurance company.
    Extracts year information from the pdf_file_url.
    """
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # get pdf content from the given url
    response = requests.get(pdf_file_url)

    if response.status_code != 200:
        raise Exception(f"Failed to download the file from {pdf_file_url}")

    # extract infromation about year (`unkown` if not found)
    with io.BytesIO(response.content) as stream:
        pdf_text = extract_text(stream, page_numbers=[0])

    year_info = re.search(re.compile(r'\b20\d{2}\b'), pdf_text)
    year = year_info.group() if year_info is not None else 'unkown'

    # define the name of the pdf file according to the specified format
    filename = f"{year}_SFCR_{company_code}_{company_name}.pdf"

    with open(os.path.join(destination_dir, filename), 'wb') as file:
        file.write(response.content)

def run(destination_dir, df, company):
    """
    Used in the main.py file to run the scraper.
    """
    years = [2018, 2019, 2020, 2021, 2022]
    df = df[df['NAZWA ZAKŁADU'] == company]
    for _, row in df.iterrows():
        company_site = row['LINK DO STRONY ZAKŁADU']
        company_code = row['KOD LEI ZAKŁADU']
        company_name = row['NAZWA ZAKŁADU']
        try:
            pdf_urls = []
            for year in stqdm(years):
                print(company_site, year)
                query = f'"Sprawozdanie o wypłacalności i kondycji finansowej" OR "Solvency and financial condition report" OR "Sprawozdanie na temat wypłacalności i kondycji finansowej" OR "SFCR" site:{company_site} filetype:pdf {company_name} {year}'
                pdf_urls += get_all_links_pdfs(query, company_site)

            pdf_urls = list(set(pdf_urls))
            for pdf_url in stqdm(pdf_urls):
                save_scrf_file(pdf_url, company_code, company_name,
                                destination_dir=os.path.join(destination_dir, company_name))
        except Exception as e:
            print(e)
            time.sleep(10)

def main(args):
    df = pd.read_csv(args.data_path, sep=';')
    years = [2018, 2019, 2020, 2021, 2022]
    for _, row in df.iterrows():
        company_site = row['LINK DO STRONY ZAKŁADU']
        company_code = row['KOD LEI ZAKŁADU']
        company_name = row['NAZWA ZAKŁADU']
        try:
            pdf_urls = []
            for year in years:
                print(company_site, year)
                query = f'"Sprawozdanie o wypłacalności i kondycji finansowej" OR "Solvency and financial condition report" OR "Sprawozdanie na temat wypłacalności i kondycji finansowej" OR "SFCR" site:{company_site} filetype:pdf {company_name} {year}'
                pdf_urls += get_all_links_pdfs(query, company_site)

            pdf_urls = list(set(pdf_urls))
            if args.pdf_downloader == 'yes':
                for pdf_url in pdf_urls:
                    save_scrf_file(pdf_url, company_code, company_name,
                                    destination_dir=args.destination_dir)
            with open(args.destination_dir+'output.txt', 'a') as f:
                for pdf_url in pdf_urls:
                    f.write(pdf_url + '\n')
        except Exception as e:
            print(e)
            time.sleep(10)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Your script description')
    parser.add_argument('--data_path', type=str, default='data/zaklady.csv', help='Path to the CSV file')
    parser.add_argument('--destination_dir', type=str, default='./data/sfcr/', help='Directory to save PDF files')
    parser.add_argument('--pdf_downloader', type=str, default='yes', help='Whether to download PDF files')
    args = parser.parse_args()
    main(args)
