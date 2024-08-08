import time
import csv
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium_stealth import stealth
from proxyscrape import create_collector

collector = create_collector('default3', 'http')


def get_proxy():
    proxy = collector.get_proxy({'country': 'united states'})
    if proxy:
        return f"http://{proxy.host}:{proxy.port}"
    return None

def get_driver(proxy=None, headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(f'user-agent={UserAgent().random}')
    
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.navigator.chrome = {
                runtime: {},
            };
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        '''
    })

    return driver

def write_to_csv(csv_file, headers, data):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerow(data)

def scrape_page(page, csv_file, headers, proxy=None, headless=False):
    driver = get_driver(proxy, headless)
    try:
        url = f'https://www.nordstrom.com/browse/women/clothing?breadcrumb=Home%2FWomen%2FClothing&origin=topnav&page={page}'
        driver.get(url)

        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//article[contains(@class, "zzWfq RpUx3")]'))
        )

        time.sleep(random.uniform(5, 10))

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        articles = soup.find_all('article', class_='zzWfq RpUx3')

        for article in articles: #Finds the features for each product
            try:
                name_element = article.find('h3', class_='kKGYj Y9bA4').find('a')
                name = name_element.text.strip()
                product_url = "https://www.nordstrom.com" + name_element['href']

                brand_element = article.find('div', class_='KtWqU jgLpg Y9bA4 Io521')
                brand = brand_element.text.strip()
                
                price_element = article.find('span', class_='qHz0a EhCiu dls-ihm460')
                price = price_element.text.strip()
                
                image_element = article.find('img', {'name': 'product-module-image'})
                image_url = image_element['src']

                star_rating_element = article.find('span', class_='T2Mzf', role='img')
                star_rating = star_rating_element['aria-label'].strip() if star_rating_element else 'No rating'
                
                num_reviews_element = article.find('span', class_='HZv8u')
                num_reviews = num_reviews_element.text.strip() if num_reviews_element else 'No reviews'

                product = {
                    "Name": name,
                    "Brand": brand,
                    "Price": price,
                    "Image URL": image_url,
                    "Product URL": product_url,
                    "Star Rating": star_rating,
                    "Number of Reviews": num_reviews
                }

                write_to_csv(csv_file, headers, product)

                print(f"Page {page} - Name: {name}")
            except Exception as e:
                print(f"Failed to scrape a product entry on page {page}: {e}")

    except Exception as e:
        print(f"Failed to load page {page} with proxy {proxy}: {e}")
        driver.save_screenshot(f'error_page_{page}.png')
        return False
    finally:
        driver.quit()
    return True

csv_file = 'product_data_nordstrom4.csv'

headers = ["Name", "Brand", "Price", "Image URL", "Product URL", "Star Rating", "Number of Reviews"]

def main():
    start_page = 1
    end_page = 500  # Define the range of pages you want to scrape

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for page in range(start_page, end_page + 1):
            proxy = get_proxy()  # Gets a new proxy for each page
            futures.append(executor.submit(scrape_page, page, csv_file, headers, proxy, True))

        for future in as_completed(futures):
            if not future.result():
                print("One of the scraping tasks failed.")

if __name__ == "__main__":
    main()
