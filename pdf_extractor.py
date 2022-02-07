from attr import s
import requests, json
import re
import pandas as pd
import pytesseract as pt

from bs4 import BeautifulSoup
from pdf2image import convert_from_bytes

def getText(url):
    text = ''
    response = requests.get(url, stream = True)

    cnt = 0
    pages = convert_from_bytes(response.raw.read())
    for i in pages:
        text += pt.image_to_string(i, lang='hin+mar+eng') + '\n'
        cnt += 1

    print(f'Pages extracted: {cnt}' + '\n')
    return text

def getActualPDF(link):
    response = requests.get(url = link)
    soup = BeautifulSoup(response.content, 'html.parser')

    for url in soup.find_all('a'):
        try:
            if url.get('href').endswith('.pdf'):
                return url.get('href')
        except:
            pass
        

if __name__ == '__main__':
    # allLinks = pd.read_csv('data/PDF_url_list_test.csv', header = None)
    allLinks = pd.read_csv('data/PDF_url_list.csv', header = None)
    allLinks = list(allLinks.iloc[:, 0])

    pdfs_json = []
    n = len(allLinks)

    for i in range(n):
        link = allLinks[i]
        if not link.endswith('.pdf'):
            allLinks[i] = getActualPDF(link)

    for link in allLinks:
        if link != None:
            pdf_url = link
            print(f'Resolving url: {pdf_url}')
            pdfs_json.append({
                "page-url": link,
                "pdf-url": pdf_url,
                "pdf-content": getText(pdf_url)
            })
            
    with open('data/pdf_extract.json', 'w') as outfile:
        json.dump(pdfs_json, outfile)
            
