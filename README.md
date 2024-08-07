<h1>Code Details</h1><br>
Run the python script scraper.py. It takes around ~10 hours to scrape 20000 product data(as mentioned in the assignment) and store it in a .csv file. 
What the code does?
It uses **Selenium** to open websites and locate the required portions(product data). Since, using 1 IP address will cause Nordstrom website to block this code after a while, this code takes help of extracting **proxy IP addresses** from other sources and uses that to extract data from website(nordstrom). 
Also, it uses **Multi Threading** to speed up the process. 
