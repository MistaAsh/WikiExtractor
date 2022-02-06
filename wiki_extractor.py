import requests, json
import re
import argparse

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def clean(text):
	text = re.sub(r'\[\d+\]', '', text)
	return text[:len(text) - 1]


def google_link_scraper(keyword, num_urls):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    query = 'site:en.wikipedia.org+' + keyword

    links = []
    cnt, page = 0, 1

    while page <= 10 and cnt < num_urls + 5:
        url = "http://www.google.com/search?q=" + query + "&start=" + str((page - 1) * 10)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        search = soup.find_all('div', class_="yuRUbf")

        for h in search:
            link = h.a.get('href')
            if 'en.wikipedia.org' in link:
                links.append(link)
                cnt += 1

                if cnt == num_urls:
                    break
        page += 1

    return links


def returnDict(url):
    response = requests.get(url = url)
    soup = BeautifulSoup(response.content, 'html.parser')

    allp = soup.find(id = 'bodyContent').find_all('p')
    if len(allp) == 0:
        return -1

    firstp = allp[0]
    for i in range(len(allp)):
        if len(allp[i].text) >= 50:
            firstp = allp[i]
            break

    if len(firstp.text) < 50:
        return -1

    return {
        'url': url,
        'paragraph': clean(firstp.text)
    }


if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description = "An addition program")
    parser.add_argument("--keyword", type = str, nargs = 1, metavar = "keyword", default = None,
                            help = "Keyword to be used for the program")
    parser.add_argument("--num_urls", type = int, nargs = 1, metavar = "num_urls", default = None,
                            help = "Number of urls to be used for the program")
    parser.add_argument("--output", type = str, nargs = 1, metavar = "output", default = None,
                            help = "Output JSON file to be used for the program")

    args = parser.parse_args()  
    if args != None:
        keyword = args.keyword[0]
        num_urls = args.num_urls[0]
        output_file = args.output[0]

        json_object = []

        allLinks = google_link_scraper(keyword, num_urls)
        allLinks = set(allLinks)

        for link in allLinks:
            output = returnDict(link)
            if type(output) == type(1):
                continue
            json_object.append(output)

        with open(output_file, 'w') as outfile:
            json.dump(json_object, outfile, indent = 4)

    print(f'Done! {len(json_object)} urls were scraped and added to the JSON file.')