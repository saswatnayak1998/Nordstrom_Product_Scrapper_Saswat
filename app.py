import asyncio
import json
from nested_lookup import nested_lookup
from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse

SCRAPFLY = ScrapflyClient(key="16eae084cff64841be193a95fc8fa67dso")

def find_hidden_data(response: ScrapeApiResponse) -> dict:
    """extract hidden web cache from page html"""
    # use XPath to find script tag with data
    data = response.selector.xpath("//script[contains(.,'__INITIAL_CONFIG__')]/text()").get()
    data = data.split("=", 1)[-1].strip().strip(";")
    data = json.loads(data)
    return data


async def scrape_product(url: str):
    response = await SCRAPFLY.async_scrape(ScrapeConfig(
        url=url,
        asp=True,  # enable anti-scraping-protection bypass
        cache=True,  # enable cache while we develop
        debug=True,  # enable debug mode while we develop
    ))
    # find all hidden dataset:
    data = find_hidden_data(response)
    # extract only product data from the dataset
    # find first key "stylesById" and take first value (which is the current product)
    product = nested_lookup("stylesById", data)
    product = list(product[0].values())[0]
    return product

# example scrape run:
print(asyncio.run(scrape_product("https://www.nordstrom.com/s/nike-phoenix-fleece-crewneck-sweatshirt/6665302")))