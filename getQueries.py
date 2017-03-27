#getQueries.py
#queries a search result through amazon.com's search engine
#returns an object list of the top results

from lxml import html
import requests
import re

XPATH_NAME = '//h1[@id="title"]//text()'
XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
NUMQUERY = 5
REQ = "http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
#XPATH_NAME = tree.xpath('//div[@title="buyer-name"]/text()')


class results(object):
	product_names = []
	product_prices = []
	product_categories = []
	products = []
	user_query = []
	all_queries = []

	def __init__(self):
		with open('reqs.txt', 'r') as reqs:
			user_query = reqs.read()
			user_query = user_query.split('\n')

		for i,w in enumerate(user_query):
			if (w):
				w = re.sub(r"\s+", '+', w)
				self.all_queries.append(w)
		print self.all_queries


	def search_query(self):
		for i,w in enumerate(self.all_queries):
			if(w):
				req = REQ
				req = req + ('%s' % str(w))
	
				page = requests.get(req,headers=headers)
				#page.raise_for_status()			
				tree = html.fromstring(page.content)
				print tree

				self.product_names.append(tree.xpath(XPATH_NAME))
				self.product_prices.append(tree.xpath(XPATH_SALE_PRICE))
				self.product_categories.append(tree.xpath(XPATH_CATEGORY))
				print self.product_names, self.product_prices, self.product_categories 
				self.products.append("%s %s %s" % (self.product_names, self.product_prices, self.product_categories))
		return self.products

if __name__ == "__main__":

    amzn = results()
    quer = []
    print amzn.search_query()
    #print quer



"""
	python script load up search results
		parse through for links to product pages
			load up individual product 
	seller
	rating

	resultscol element in html
"""