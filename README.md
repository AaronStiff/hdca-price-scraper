# hdca-price-scraper
A Python script to scrape product prices from HomeDepot.ca

# Dependencies

`urllib3` and `certifi`

To install with `pip`: `pip install urllib3 certifi`

# Usage

Products and their associated IDs should be stored in `product_id.txt`, separated by a comma (see `product_id.txt` for examples)

Product IDs can currently be found at the end of the HomeDepot.ca URL, e.g.

`https://www.homedepot.ca/product/2-inch-x-4-inch-x-8-ft-spf-dimensional-lumber/1000112108` <---

where the ID is `1000112108`

When run, an interactive menu will be provided to run the available commands, which include fetching the price of one or all listed products, displaying all listed product names, and applying a discount to all prices. 
