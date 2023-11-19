from bs4 import BeautifulSoup
import os
import re
import requests

class WebsiteScrapper:
    def __init__(self) -> None:
        self.search_keywords = ['Sprawozdanie o wypłacalności i kondycji finansowej', 'sfcr']

    def download_pdfs(self, url: str, directory: str ='./scraped_files'):
        if os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        links = soup.find_all(['a', 'span', 'p'], href=re.compile(r'\.pdf$'))
        print(links)
        matching_links = [link for link in links if any(keyword.lower() in link.get_text().lower() for keyword in self.search_keywords)]

        for link in matching_links:
            if link.name == 'a':
                pdf_url = link.get('href')
            elif link.name == 'span':
                pdf_url = link.find('a', href=True).get('href')
            elif link.name == 'p':
                pdf_url = link.find('span').find('a', href=True).get('href')
            filename = os.path.join(directory, pdf_url.split('/')[-1])
            with open(filename, 'wb') as file:
                file.write(requests.get(pdf_url).content)
                print(f"Downloaded: {pdf_url}")