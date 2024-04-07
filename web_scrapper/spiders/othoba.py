import re
from random import randint
import time
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from lxml import etree
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


class OthobaSpider(scrapy.Spider):
    """
    A Scrapy spider for scraping data from the Othoba website.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): The list of allowed domains for the spider.
        start_urls (list): The list of start URLs for the spider.
        visited_urls (set): Set to store visited product URLs.
        df (list): The list to store the scraped data.

    Methods:
        __init__(self, name=None, **kwargs): Initializes the spider.
        start_requests(self): Generates the initial request to start scraping.
        parse(self, response): Parses the response and extracts the desired data.
        scrape_data(self, driver): Scrapes the data from each product element.
        closed(self, reason): Handles the spider closed event and saves the scraped data to a CSV file.
    """

    name = "othoba"
    allowed_domains = ["www.othoba.com"]

    def __init__(self, name=None, **kwargs):
        """
        Initializes the lists and sets required for scraping.

        Args:
            name (str): The name of the spider.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        super().__init__(name=name, **kwargs)
        self.start_urls = ["https://www.othoba.com/smartphone?orderby=0&pagesize=40"]
        self.visited_urls = set()
        self.df = []

    def start_requests(self):
        """
        Generates the initial request to start scraping.

        Returns:
            SeleniumRequest: The initial request to start scraping.
        """
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=randint(8, 12),
                wait_until=EC.presence_of_element_located((By.CLASS_NAME, 'pagination'))
            )

    def parse(self, response):
        """
        Parses the response and extracts the desired data.

        Args:
            response (scrapy.http.Response): The response object.

        Returns:
            None
        """
        driver = response.request.meta['driver']
        self.scrape_data(driver)

        while True:
            try:
                next_page_element = driver.find_element(By.XPATH, '//li[@class="page-item active"]/following-sibling::li/a')
                next_page_url = next_page_element.get_attribute("href")
                print(f"Next Page's URL: {next_page_url}")
                if next_page_url not in self.visited_urls:
                    self.visited_urls.add(next_page_url)
                    driver.get(next_page_url)
                    self.scrape_data(driver)
                else:
                    print("All mobile details link scrapped.")
                    break
                self.visited_urls.add(next_page_url)
            except NoSuchElementException:
                print("Scrapping completed.")
                break
            time.sleep(randint(3, 7))

    def scrape_data(self, driver):
        """
        Scrapes the data from each product element on the current page.

        Args:
            driver (selenium.webdriver.Chrome): The Selenium WebDriver instance.

        Returns:
            None
        """

        # lambda function to extract numbers using regex from a string
        extract_number = lambda element: re.sub(r"[^\d,]", "", element).strip() if element else None

        # Select all product elements and iterate over them
        for product in driver.find_elements(By.XPATH, '//*[@class="product product-image-gap product-simple"]'):
            # Scrape the desired data from each product
            product_name_link = product.find_element(By.CLASS_NAME, "product-name")
            product_details_link = product_name_link.find_element(By.TAG_NAME, "a").get_attribute("href")
            product_title = product.find_element(By.CLASS_NAME, "product-name").text

            if product_details_link not in self.visited_urls:
                self.visited_urls.add(product_details_link)
                # Call BeautifulSoup to get the product details
                req = requests.get(product_details_link, timeout=30)
                # Passing the requested content to Beautiful Soup
                product_soup = BeautifulSoup(req.content, "html.parser")
                dom = etree.HTML(str(product_soup))

                # If product specifications are not available, skip the product
                if dom.xpath('//*[@id="product-tab-specification"]/ul/li') == []:
                    continue

                ram = dom.xpath('//*[@id="product-tab-specification"]/ul/li[2]/p')[0].text
                ram = re.sub(r"[^\d\w,]", " ", ram).strip()

                storage_dom = dom.xpath('//*[@id="product-tab-specification"]/ul/li[3]/p')
                storage = None
                if storage_dom:
                    storage = storage_dom[0].text.strip()

                display_dom = dom.xpath('//*[@id="product-tab-specification"]/ul/li[4]/p')
                display = None
                if display_dom:
                    display = display_dom[0].text.strip()

                phone_color_dom = dom.xpath('//*[@id="product-tab-specification"]/ul/li[1]/p')
                phone_color = None
                if phone_color_dom:
                    phone_color = phone_color_dom[0].text.strip()

                operating_system_dom = dom.xpath('//*[@id="product-tab-specification"]/ul/li[5]/p')
                operating_system = None
                if operating_system_dom:
                    operating_system = operating_system_dom[0].text.strip()

                current_price = product.find_element(By.XPATH, '//*[@class="new-price dl-new-price-product"]').text
                if current_price:
                    # current_price = re.sub(r"[^\d,]", "", current_price).strip()
                    current_price = extract_number(current_price)

                old_price = product.find_element(By.XPATH, '//*[@class="old-price"]').text
                if old_price:
                    # old_price = re.sub(r"[^\d,]", "", old_price).strip()
                    old_price = extract_number(old_price)

                # avg_rating = dom.xpath('//*[@id="product-details-form"]/div/div[3]/div/span[2]')[0].text
                total_reviews = dom.xpath('//*[@id="product-details-form"]/div/div[3]/a')[0].text
                # total_reviews = re.sub(r"[^\d,]", "", total_reviews)
                total_reviews = extract_number(total_reviews)

                brand_name = dom.xpath('//*[@id="product-details-form"]/div/div[1]/div/div[2]/div[2]/span[2]/a')[0].text
                seller = dom.xpath('//*[@id="product-details-form"]/div/div[1]/div/div[2]/div[3]/span[2]/a')[0].text
                seller_rating = dom.xpath('//*[@class="sold-info seller-statting"]/p[2]')[0].text
                ship_on_time = dom.xpath('//*[@class="sold-info seller-ship"]/p[2]')[0].text

                result = {
                    "product_details_link": product_details_link,
                    "product_title": product_title,
                    "ram": ram,
                    "storage": storage,
                    "display": display,
                    "phone_color": phone_color,
                    "operating_system": operating_system,
                    "current_price": current_price,
                    "old_price": old_price,
                    # "avg_rating": avg_rating,
                    "total_reviews": total_reviews,
                    "brand_name": brand_name,
                    "seller": seller,
                    "seller_rating": seller_rating,
                    "ship_on_time": ship_on_time
                }
                pprint(result)

                # append the scraped data to the list of scraped items
                self.df.append(result)

    def closed(self, reason):
        """
        Handles the spider closed event and saves the scraped data to a CSV file.

        Args:
            reason (str): The reason why the spider was closed.

        Returns:
            pandas.DataFrame: The scraped data as a pandas DataFrame.
        """
        df = pd.DataFrame(self.df)
        df.to_csv("datasets/othoba_products.csv", index=False)
        return df
    