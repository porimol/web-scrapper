from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from web_scrapper.spiders.othoba import OthobaSpider


def main():
    """
    This function is the entry point of the web scraping process.
    It creates a CrawlerProcess, runs a spider, retrieves the scraped items,
    converts them to a DataFrame, and prints the head of the DataFrame.
    """
    
    # Create a CrawlerProcess
    process = CrawlerProcess(get_project_settings())

    # Create an empty list to store the scraped items
    items = []

    # Define a callback function to retrieve the scraped items
    def get_items(result, spider):
        items.extend(result)

    # Run the spider and pass the callback function
    process.crawl(OthobaSpider, items=items, callback=get_items)
    process.start()


if __name__ == "__main__":
    main()
