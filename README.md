# WikiExtractor

<img src="https://img.shields.io/github/license/MistaAsh/WikiExtractor"> <img src="https://img.shields.io/github/languages/top/MistaAsh/WikiExtractor"> <img src="https://img.shields.io/github/issues/MistaAsh/WikiExtractor"> <img src="https://img.shields.io/github/issues-pr/MistaAsh/WikiExtractor"> <img src="https://img.shields.io/github/last-commit/MistaAsh/WikiExtractor">


This is WikiExtractor! A simple and easy to use Python-based Web Scraping tool that can be used to extract information from Wikipedia pages.

## Installation
To contribute and work on the repository, you need Python installed on your system. If you do not have Python installed, you can install it from [here](https://www.python.org/downloads/).

Fork and clone the repository from GitHub.
```bash
git clone https://github.com/<your-username-here>/WikiExtractor.git
```

Traverse to the directory where the repository is cloned.
```bash
cd WikiExtractor
```

To execute the script, you will need to install the dependencies. It is recommended to create a virtual environment to do the same
```bash
virtualenv venv
pip install -r requirements.txt
```

Use the following command to run the script.
```bash
python WikiExtractor.py --keyword=<your_keyword> --num_urls=<your_num_urls> --output=<your_output_JSON_file>
```
Replace each `<>`with the appropriate values. Make sure to append `.json` to the end of the output file name to prevent any errors.

## Implementation

The implementation of WikiExtractor is done in Python. The code is written in a modular way so that it can be easily integrated into other projects.

The extractor tool leverages the Search Optimization of the Google search engine to give the user the best possible results. It initially sends a `GET` request to the Google search engine with the query as the search term. The search engine returns a list of Wikipedia URLs that are relevant to the search term. The extractor then sends a `GET` request to each of the URLs and extracts the relevant information from the HTML page.
