# Web Scrapping Project

Our project involves scraping mobile phone details from [Othoba](https://www.othoba.com/smartphone?orderby=0&pagesize=40) using Python's Scrapy, Selenium, Requests, BeautifulSoup, regex, and lambda functions to demonstrate data extraction and manipulation techniques.

## Project Overview

Our project involves scraping mobile phone details from Othoba, an online marketplace. We utilized a combination of web scraping tools and libraries, including Scrapy, Selenium, Requests, and BeautifulSoup in Python. Through this project, we aimed to demonstrate our proficiency in data extraction and web scraping techniques.

To extract and process the data efficiently, we used various methods such as Scrapy spiders for navigating through the website, Selenium for dynamic content rendering, and BeautifulSoup for parsing HTML content to extract phone's details. Additionally, we utilized Python's regex and lambda functions to extract specific information from the scraped data.

Overall, our project showcases our ability to effectively gather and analyze data from online sources, demonstrating key concepts in web scraping and basic data manipulation using Python.

## Teammates

- Porimol Chandro
- Patilda G Baluka

## Python Version

Minimum python version should have 3.11.x or upper

## List of Python Packages

```bash
python              = "^3.11"
pandas              = "^2.2.1"
requests            = "^2.31.0"
beautifulsoup4      = "^4.12.3"
lxml                = "^5.2.1"
scrapy              = "^2.11.1"
selenium            = "^4.19.0"
webdriver-manager   = "^4.0.1"
pandas-stubs        = "^2.2.1.240316"
```

## Project structure

The project structure consists of the following components:

```bash
.
├── README.md
├── datasets
│   └── othoba_products.csv
├── main.py
├── poetry.lock
├── pyproject.toml
├── scrapy.cfg
├── scrapy_selenium
│   ├── __init__.py
│   ├── http.py
│   └── middlewares.py
└── web_scrapper
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── othoba-product-details.ipynb
    ├── pipelines.py
    ├── settings.py
    └── spiders
        ├── __init__.py
        └── othoba.py
```

- **README.md:** A Markdown file containing information about the project.
- **datasets:** A directory containing the CSV file `othoba_products.csv`, which likely stores scraped data.
- **main.py:** A Python script that may contain the main entry point or functionality of the project.
- **poetry.lock and pyproject.toml:** Files related to dependency management using Poetry.
- **scrapy.cfg:** Configuration file for Scrapy, a web crawling and scraping framework.
- **scrapy_selenium:** A Python package or module containing code related to Selenium integration with Scrapy.
    - **http.py:** Initialize a new selenium request.
    - **middlewares.py:** Middleware component for request and response processing in `Scrapy` using `Selenium`.
- **web_scrapper:** A Python package or module that appears to be the main project directory, including the following files and directories:
    - **init.py:** An empty file indicating that web_scrapper is a Python package.
    - **items.py:** File containing item classes for Scrapy, defining the structure of scraped data.
    - **middlewares.py:** File containing middleware components, likely for request and response processing in Scrapy.
    - **othoba-product-details.ipynb:** Jupyter Notebook file, possibly used for scraping Othoba website product details.
    - **pipelines.py:** File containing pipelines for processing scraped items in Scrapy.
    - **settings.py:** Configuration file for Scrapy settings.
    - **spiders:** A directory containing Scrapy spiders, including:
        - **init.py:** An empty file indicating that spiders is a Python package.
        - **othoba.py:** A Python file containing a Scrapy spider, likely for scraping product details from the Othoba website.

## How to get set up?

To manage Python dependencies, we used [Python Poetry](https://python-poetry.org/docs/), that's why you must need to install `Python Poetry` first.

### Installation

Install all of the necessary Python packages using the following command.

```bash
poetry install
```

Now you need to activate virtual environment created by Poetry. Activating the virtual environment, use the following command.

```bash
poetry shell
```

### Scrapping

To initiate the scraper, there are two methods available:

- Using Scrapy's built-in command:

    ```bash
    scrapy crawl othoba
    ```

- Executing the Python script directly:

    ```bash
    python main.py
    ```

Please be patient while the scraping process completes.

## Disclaimer

The information provided in this project is for educational and learning purposes only. We do not endorse or encourage any unethical activities, including but not limited to unauthorized scraping of data.

The mobile phone details scraped from [Othoba](https://www.othoba.com/smartphone?orderby=0&pagesize=40) were solely used to demonstrate our understanding and skills in web scraping and data analysis. We acknowledge that scraping data from websites without proper authorization may violate terms of service and legal regulations.

We respect the rights of website owners and encourage ethical data collection practices.

We deleted all information that we scrapped for our learning purpose.
