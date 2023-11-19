import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import pickle

"""
script for demo purposes only
"""

def main():
    response = requests.get('https://www.nn.pl/notowania-i-wyniki-finansowe/raporty-finansowe')
    soup = BeautifulSoup(response.text, 'html.parser')
    pp = soup.find('div', class_='row align-center')

    docs = {}

    for p in pp.find_all('p'):
        link = p.find('a')
        nazwa = p.find('span')
        if nazwa is None:
            continue
        if link is None:
            year = nazwa.text
            docs[nazwa.text] = []
            print(nazwa.text)
        else:
            print('www.nn.pl'+link.get('href'))
            print(nazwa.text[2:].strip(" - pobierz"))
            docs[year].append(('www.nn.pl'+link.get('href'), nazwa.text[2:].strip(" - pobierz")))

    with open('nn.pickle', 'wb') as f:
        pickle.dump(docs, f)

if __name__ == "__main__":
    main()
