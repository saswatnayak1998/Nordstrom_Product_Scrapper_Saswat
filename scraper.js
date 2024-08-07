const puppeteer = require('puppeteer');
const fs = require('fs');
const csvWriter = require('csv-writer').createObjectCsvWriter;

// CSV setup
const csvFile = 'nordstrom_products.csv';
const csvHeaders = [
    { id: 'Name', title: 'Name' },
    { id: 'Brand', title: 'Brand' },
    { id: 'Price', title: 'Price' },
    { id: 'Image URL', title: 'Image URL' },
    { id: 'Product URL', title: 'Product URL' },
    { id: 'Star Rating', title: 'Star Rating' },
    { id: 'Number of Reviews', title: 'Number of Reviews' }
];

const writer = csvWriter({ path: csvFile, header: csvHeaders });

(async () => {
    const browser = await puppeteer.launch({ headless: false }); // Set to false to see the browser actions
    const page = await browser.newPage();
    const baseUrl = 'https://www.nordstrom.com/browse/women/clothing?breadcrumb=Home%2FWomen%2FClothing&origin=topnav&page=';

    let products = [];
    const numPages = 5; // Adjust the number of pages you want to scrape

    for (let pageNum = 1; pageNum <= numPages; pageNum++) {
        const url = `${baseUrl}${pageNum}`;
        await page.goto(url, { waitUntil: 'networkidle2' });

        // Wait for the articles to load
        await page.waitForSelector('article.zzWfq.RpUx3');

        const productData = await page.evaluate(() => {
            const articles = document.querySelectorAll('article.zzWfq.RpUx3');
            let productArray = [];
            articles.forEach(article => {
                const nameElement = article.querySelector('h3.kKGYj.Y9bA4 a');
                const name = nameElement ? nameElement.innerText.trim() : 'N/A';
                const productUrl = nameElement ? `https://www.nordstrom.com${nameElement.getAttribute('href')}` : 'N/A';
                const brandElement = article.querySelector('div.KtWqU.jgLpg.Y9bA4.Io521');
                const brand = brandElement ? brandElement.innerText.trim() : 'N/A';
                const priceElement = article.querySelector('span.qHz0a.EhCiu.dls-ihm460');
                const price = priceElement ? priceElement.innerText.trim() : 'N/A';
                const imageElement = article.querySelector('img[name="product-module-image"]');
                const imageUrl = imageElement ? imageElement.getAttribute('src') : 'N/A';
                const starRatingElement = article.querySelector('span.T2Mzf[role="img"]');
                const starRating = starRatingElement ? starRatingElement.getAttribute('aria-label').trim() : 'No rating';
                const numReviewsElement = article.querySelector('span.HZv8u');
                const numReviews = numReviewsElement ? numReviewsElement.innerText.trim() : 'No reviews';

                productArray.push({
                    Name: name,
                    Brand: brand,
                    Price: price,
                    'Image URL': imageUrl,
                    'Product URL': productUrl,
                    'Star Rating': starRating,
                    'Number of Reviews': numReviews
                });
            });
            return productArray;
        });

        products = products.concat(productData);
        
        // Random delay between requests to mimic human behavior
        await page.waitForTimeout(Math.floor(Math.random() * 30000) + 10000);
    }

    await writer.writeRecords(products);
    console.log(`Data saved to ${csvFile}`);

    await browser.close();
})();
