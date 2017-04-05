#getQueries.py
#queries a search result through amazon.com's search engine
#returns an object list of the top results

from lxml import html
import requests
import re
import logging
import urllib2

XPATH_NAME = './/h2/text()'
XPATH_LINK = './/a[class="a-link-normal a-text-normal"]/@href'
#XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
XPATH_PRICE = '//a[@class="a-link-normal a-color-tertiary"]//text()'
XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

#Website Constants
#Specify which web query and browser emulator here
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
BASE_URL = "http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="

#specify number of products crawled per item
NUM_PRODUCTS = 1

class results(object):
	def __init__(self):
		self.items = []
		self.product_names = ""
		self.product_links = ""
		self.product_prices = ""
		self.products = []
		
		self.user_query = []
		self.all_queries = []
		
		with open('reqs.txt', 'r') as reqs:
			self.user_query = (reqs.read()).split('\n')
			
		for w in (self.user_query):
			if (w):
				w = re.sub(r"\s+", '+', w)
				self.all_queries.append(w)
		print self.all_queries


	def search_query(self):
		for w in self.all_queries:
			if(w):
				req = BASE_URL
				req = req + ('%s' % str(w))

				#pull html from the webpage request through amazon
				page = requests.get(req,headers=headers)
				#page.raise_for_status()	#for error codes		
				tree = html.fromstring(page.content)
				
				#Iterate through the specified # of results
				for i in range(NUM_PRODUCTS):
					XPATH_BASE = '//li[@id="result_' + str(i) + '"]'
					self.items.append(tree.xpath(XPATH_BASE))
					#print self.items[i]
				
				#iterate through each product result on amazon 0x7fa183258310> 0x7f92531ad2b8>
				for item in self.items:
					#print item[0].xpath(XPATH_NAME)
					self.product_names = item[0].xpath(XPATH_NAME)
					self.product_links = item[0].xpath(XPATH_LINK)
					self.product_prices = item[0].xpath(XPATH_PRICE)
					self.products.append("%s %s %s" % (str(self.product_names), str(self.product_links), str(self.product_prices)))
				
				self.product_links = ""
				self.product_names = ""
				self.product_prices = ""
				del self.items[:]
				
		print self.products
		#return self.products

if __name__ == "__main__":

    amzn = results()
    #print amzn.search_query()
    amzn.search_query()


"""
	python script load up search results
		parse through for links to product pages
			load up individual product 
	seller
	rating

	resultscol element in html
"""
