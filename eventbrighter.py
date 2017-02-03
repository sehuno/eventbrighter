#!/bin/python
import os
import re
import pymongo
import sys
import lxml
import requests
from bs4 import BeautifulSoup

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   	'Accept-Encoding': 'none',
   	'Accept-Language': 'en-US,en;q=0.8',
   	'Connection': 'keep-alive'
}

class Event:
	def __init__(self, soup):
		self.url = soup['data-share-url'].encode('UTF-8').strip() # event url
		self.title = soup['data-share-name'].encode('UTF-8').strip() # event title
		try: # event price
			self.price = soup.a.div.span.string.encode('UTF-8').strip()
		except:
			self.price = "N/A"

		self.hashtag = [] # event hashtags
		for ht in soup.find_all('div','list-card__tags'):
			try:
				[self.hashtag.append(a_elem.string.encode('UTF-8').strip()) for a_elem in ht.find_all('a')]
			except:
				break

		# actually visit the event url to parse data
		html = requests.get(self.url, headers=hdr)
		soup = BeautifulSoup(html.text, 'lxml')

		try: # event organizer
			self.organizer = soup.find('a', 'js-d-scroll-to listing-organizer-name text-default').string.encode('UTF-8').strip()[3:]
		except:
			self.organizer = "N/A"

		self.date = soup.find('time', 'listing-hero-date')['datetime'] # event date
		try:
			self.time = soup.find('time', 'clrfix').find_all('p')[1].string.encode('UTF-8').strip()	# event time
			# MUST PERFORM CHECK OF DATE FORMAT TYPE
		except:
			self.time = "N/A"

		self.location = [] # event location
		try: #
			children = soup.find_all('div', 'event-details__data')[1].find_all('p', recursive=False)
			[self.location.append(child.string.encode('UTF-8').strip()) for child in children[:-1]]
		except:
			print "location N/A"

		print self.__dict__
		# other details that might be worth storing: image, description
		# self.print_self

	def print_self(self):
		print self.__dict__

# class SBIR_Awardee :
# 	def __init__(self, link):
# 		global year_limit_reached
# 		acceptable_cities = ["San Jose", "Sunnyvale", "Santa Clara", "Los Gatos", "Campbell", "Milpitas", "Santa Cruz", "Mountain View", "Saratoga", "Berkeley", "Los Angeles", "Santa Monica", "Palo"]
# 		html = requests.get(link, headers=hdr)
# 		self.url = link
# 		soup = BeautifulSoup(html.text,"lxml")
# 		self.title = soup.select("#main-column > div > h1")[0].string.encode('utf-8')
# 		self.year = int(soup.find_all('div', 'col-sm-3 meta-description')[1].text.strip())
# 		if self.year < 2015:
# 			year_limit_reached = True
# 			return
# 		self.amount = soup.find_all('div', 'col-sm-4 meta-description')[1].text.encode('utf-8').strip()
# 		self.company = soup.find('div', 'sbc-name-wrapper').string.encode('utf-8').strip()
# 		print "Current company: %s" % self.company
# 		self.address = soup.find('div', 'sbc-address-wrapper').string.encode('utf-8').strip()
# 		self.contact = soup.find('div', 'award-sub-description').text.encode('utf-8').strip()
# 		self.abstract = soup.find('div', 'abstract-wrapper').text.encode('utf-8')
# 		if any(acc_city.lower() in self.address.lower() for acc_city in acceptable_cities):
# 			awardees.append(self)

# def printToFiles(aList):
# 	file = open('summary.txt', 'w')
# 	for i, a in enumerate(awardees):
# 		file.write("%d %s\n\n" % (i + 1, a.title))
# 		file.write("\t%s" % a.company)
# 		file.write("\t%s" % a.amount)
# 		file.write("\t%d" % a.year)
# 		file.write("\t%s" % a.address)
# 		file.write("\n\t%s\n\n" % a.contact)
# 	for i, a in enumerate(awardees):
# 		file.write("%d %s\n" % (i + 1, a.title))
# 		file.write("%s\n\n" % a.abstract)
# 	file.close()

def main(argv):
	# print "Build an eventbrite scraper!"
	# try:
	#     connection = pymongo.MongoClient()
	#     print "Connected successfully!!!"
	# except pymongo.errors.ConnectionFailure, e:
	#    print "Could not connect to MongoDB: %s" % e
	# connection

	next_page_exists = True

	url = "https://www.eventbrite.com/d/ca--san-jose/events--this-week/"
	# url = "https://www.eventbrite.com/d/ca--san-jose/events--this-week/?crt=regular&page=43&sort=best"

	while next_page_exists:
		html = requests.get(url, headers=hdr)
		soup = BeautifulSoup(html.text, 'lxml')
		[Event(event_soup) for event_soup in soup.find_all('div','list-card-v2 l-mar-top-2 js-d-poster')]  # pass soup to event constructor

		next_page_exists = False
		# next_page_exists = soup.find('a','js-show-next is-disabled')
		# print next_page_exists

	# db = conn.mydb
	# global awardees
	# global year_limit_reached
	# awardees = []
	# year_limit_reached = False
	# # startUrl = "https://www.sbir.gov/sbirsearch/award/all/software?f[0]=im_field_state%3A105809"
	# startUrl = "https://www.sbir.gov/sbirsearch/award/all/?f[0]=im_field_state%3A105809"
	#
	# while not year_limit_reached:
	# 	html = requests.get(startUrl, headers=hdr)
	# 	soup = BeautifulSoup(html.text, 'lxml')
	# 	for is_link in soup.find_all('li','search-result'):
	# 		SBIR_Awardee("https://www.sbir.gov" + is_link.h3.a['href'])
	# 		if year_limit_reached:
	# 			break
	# 	next_page = soup.find('li', 'next').a['href']
	# 	startUrl = "https://www.sbir.gov" + next_page
	# printToFiles(awardees)

if __name__ == '__main__' :
	main(sys.argv[1:])
