#!/usr/bin/env python3

# HDCA Price Scraper, created by @AaronStiff, https://github.com/AaronStiff

# Each line of the text file containing the product names and asscoiated IDs should be of the form:
# <product_name>,<id>
# with a single comma between the two. Currently the IDs can be found at the end of a product url, e.g.
# https://www.homedepot.ca/product/2-inch-x-4-inch-x-8-ft-spf-dimensional-lumber/1000112108 <--
# Here, the product ID is "1000112108". These could easily be subject to change without notice.

import urllib3, certifi, json



def get_price_from_id(https, id, discount):
    '''
    Scrapes HomeDepot.ca for the price of a particular product

    Parameters
    ----------
    https : urllib3.PoolManager() object
        Used to make the GET request
    id : str
        Product ID to lookup
    discount : float
        Float between 0 and 1 which is multipled by the product price as a discount

    Returns
    -------
    str
        Product price with a dollar sign at the front
    '''

    # HomeDepot.ca doesn't allow scraping unless it recognizes the User-Agent
    custom_headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

    url_prefix = 'https://www.homedepot.ca/api/productsvc/v1/products/'
    url_suffix = '/store/7173?fields=BASIC_SPA&lang=en'
    url = url_prefix + id + url_suffix

    try:
        r = https.request('GET', url, headers = custom_headers)
        price = json.loads(r.data)['optimizedPrice']['displayPrice']['value']

        return '$' + str(round(price*discount, 2))
    except KeyError as e:
        return f'The ID associated with that product ({id}) is not valid!'

def read_from_file(pid_filereader):
    '''
    Generates a product/id dictionary from a _io.TextIOWrapper of the product/id file

    Parameters
    ----------
    pid_filereader : _io.TextIOWrapper
        TextIOWrapper of the product/id text file with entries in the form <product_name> <id>

    Returns
    -------
    dict {str:str,...}
        Product/id dictionary of the form {product_name:id}
    '''

    file = pid_filereader.readlines()

    product_id = {}
    for l in file:
        product, id = l.strip().split(',')
        product_id[product] = id

    return product_id

def main(pid_filereader):
    '''
    Main function responsible for the interactive menu

    Parameters
    ----------
    product_id : dict
        Catalog of products and their associated IDs
    
    '''

    https = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs = certifi.where())

    intro = '''
Choose an option:
    p: get the price of a product
    l: list all available products
    a: get the prices of all listed products
    d: set the discount factor
    q: quit

> '''

    product_id = read_from_file(pid_filereader)
    discount = 1.0
    opt = input(intro)

    while opt != 'q':
        if opt == 'p':
            id = product_id.get(input('Product name: '), None)
            if id:
                print('\n' + get_price_from_id(https, id, discount))
                
        elif opt == 'l':
            print()
            for p in product_id:
                print(p)

        elif opt == 'a':
            print()
            for p in product_id:
                print(f'{p}: {get_price_from_id(https, product_id[p], discount)}')

        elif opt == 'd':
            discount = float(input('New discount factor (decimal from 0 to 1, default is 1): '))
        
        opt = input('\n> ')

if __name__ == '__main__':
    with open('product_id.txt','r+') as pid_filereader:
        main(pid_filereader)