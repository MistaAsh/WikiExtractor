import requests, json
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def clean(text):
	text = re.sub(r'\[\d+\]', '', text)
	return text[:len(text) - 1]


def google_link_scraper(keyword, n):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--headless")

	driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
	query = 'site:en.wikipedia.org+' + keyword

	links = []
	for page in range(1, n):
		url = "http://www.google.com/search?q=" + query + "&start=" +      str((page - 1) * 10)
		driver.get(url)

		soup = BeautifulSoup(driver.page_source, 'html.parser')
		search = soup.find_all('div', class_="yuRUbf")

		for h in search:
			link = h.a.get('href')
			if 'en.wikipedia.org' in link:
				links.append(link)

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

	return {
		'url': url,
		'paragraph': clean(firstp.text)
	}

json_object = []

allLinks = google_link_scraper('spyder', 3)
allLinks = set(allLinks)

for link in allLinks:
	output = returnDict(link)
	if type(output) == type(1):
		continue
	json_object.append(output)

with open('output.json', 'w') as outfile:
	json.dump(json_object, outfile, indent = 4)