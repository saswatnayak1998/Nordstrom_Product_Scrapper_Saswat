<h1>Code Details</h1>
<p>
Run the python script scraper.py. It takes around ~10 hours to scrape 20000 product data(as mentioned in the assignment) and store it in a .csv file. 
What the code does?
It uses <b>Selenium</b> to open websites and locate the required portions(product data). Since, using 1 IP address will cause Nordstrom website to block this code after a while(and the website shows this Image- https://github.com/saswatnayak1998/Nordstrom_Product_Scrapper_Saswat/blob/main/error_page_149.png, this code takes help of extracting  <b>Other Proxy IP Addresses</b>  from other sources and uses that to extract data from website(nordstrom). 
Also, it uses <b>Multi Threading</b> to speed up the process. 
  </p>
<h1>Code Run</h1>
Simply clone the repo and run the python file

<h1>What can the code do?</h1>
<ul>It can scrape product details of the women's clothes. You can provide the page range you want to scrape.</ul>
<ul>You can change the number of multi-threading operations.</ul>
<ul>It uses a new IP address for every page it scrapes, thereby avoiding blockage by Nordstrom.</ul>
