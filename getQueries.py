#getQueries.py
#queries a search result through amazon.com's search engine
#returns an object list of the top results

from lxml import html
import requests
import re
import logging
#import urllib2
import scrapy
import os

#XPATH_NAME = '//h2/text()'
#XPATH_PRICE = './/a[@class="a-link-normal a-text-normal"]//@aria-label//text()'
#XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
#XPATH_LINK = './/a[@class="a-size-small a-link-normal a-text-normal"]/@href[1]'
XPATH_LINK = '(.//a[@class="a-size-small a-link-normal a-text-normal"]/@href)[1]'

#Website Constants
#Specify which web query and browser emulator here
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
BASE_URL = "http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="

#specify number of products crawled per item
NUM_PRODUCTS = 1

class results(object):
	def __init__(self):
		self.products = []
		
		self.user_query = []
		self.all_queries = []
		
		#read file that contains the items to be searched through online marketplaces
		if __name__ == '__main__':
			cwd = os.getcwd() + "/reqs.txt"
		else:
			cwd = os.getcwd() + "/spiders/modules/reqs.txt" #use this if running as part of scrapy spider
			
		with open(cwd, 'r') as reqs:
			self.user_query = (reqs.read()).split('\n')
			
		#format each item query to replace whitespace with "+"s
		for w in (self.user_query):
			if (w):
				w = re.sub(r"\s+", '+', w)
				self.all_queries.append(w)
		print self.all_queries


	def search_query(self):
		product_names = ""
		product_links = ""
		
		for w in self.all_queries:
			if(w):
				#for each search on an online marketplace, append the specific search query
				req = BASE_URL
				req = req + ('%s' % str(w))
				
				#pull html from the webpage request through amazon
				page = requests.get(req,headers=headers)
				#page.raise_for_status()	#for error codes
				
				#pull the html from the retrieved webpage
				tree = html.fromstring(page.content)
				
				#Iterate through the specified # of results per query
				for i in range(NUM_PRODUCTS):
					XPATH_BASE = '//li[@id="result_' + str(i) + '"]'
					#for item in tree.xpath(XPATH_BASE):
					items = tree.xpath(XPATH_BASE)
					#print tree.xpath(XPATH_BASE)
				
					#print items
					#iterate through each product result on amazon
					
					product_links = items[0].xpath(XPATH_LINK) #good?
					self.products.append(product_links)
					#print self.products
						
					product_links = ""
					product_names = ""
					
				del items[:]
		#print self.products		
		return self.products
				
if __name__ == "__main__":

    amzn = results()
    #print amzn.search_query()
    print amzn.search_query()


"""
	python script load up search results
		parse through for links to product pages
			load up individual product 
	seller
	rating

	resultscol element in html
"""
