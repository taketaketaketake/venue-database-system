import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

def scrape_website(url):
    try:
        events = []

        class EventSpider(scrapy.Spider):
            name = "event_spider"
            start_urls = [url]

            def __init__(self, events_list, **kwargs):
                super().__init__(**kwargs)
                self.events_list = events_list

            def parse(self, response):
                for event in response.css(".event-item"):
                    name = event.css(".event-title::text").get()
                    date = event.css(".event-date::text").get()
                    link = event.css("a::attr(href)").get()

                    if name and date:
                        self.events_list.append({
                            "name": name.strip(),
                            "date": date.strip(),
                            "url": response.urljoin(link) if link else response.url
                        })

        settings = Settings()
        settings.set('LOG_ENABLED', False)

        process = CrawlerProcess(settings)
        process.crawl(EventSpider, events_list=events)
        process.start()

        return events

    except Exception as e:
        logging.error(f"Scraping error for {url}: {e}")
        return []

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    url = "https://example.com/events"
    events = scrape_website(url)
    for e in events:
        print(e)

def scrape_dynamic_website(url, llm_func):
    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        content = driver.page_source
        driver.quit()
        events = llm_func(content, url)
        logging.info(f"Scraped dynamic website: {url}")
        return events
    except Exception as e:
        logging.error(f"Dynamic scraping error for {url}: {e}")
        return []
