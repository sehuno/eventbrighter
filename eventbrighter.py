#!/bin/python
import os
import re
import pymongo
import sys
import json
import thread
import lxml
import requests
from datetime import *
from bs4 import BeautifulSoup

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   	'Accept-Encoding': 'none',
   	'Accept-Language': 'en-US,en;q=0.8',
   	'Connection': 'keep-alive'
}

global coll

def dateTime():
	today = datetime.today()
	return "Week %s" % today.strftime("%U").lstrip("0")

def connectToDB():
	try:
		client = pymongo.MongoClient("localhost", 27017)
	except:
		print "Could not connect to MongoDB"
	db = client.eventbrite
	global coll
	coll = db[dateTime()]

	# d = dict((db, [dbection for dbection in client[db].dbection_names()])
    # for db in client.database_names())
    # 	print json.dumps(d)

def parse_eventbrite():
	url = "https://www.eventbrite.com/d/ca--san-jose/events--this-week/"
	# url = "https://www.eventbrite.com/d/ca--san-jose/events--this-week/?crt=regular&page=43&sort=best"
	# should also include option of parsing different eventbrite pages (free, paid, different city)

	next_page_exists = True
	while next_page_exists:
		html = requests.get(url, headers=hdr)
		soup = BeautifulSoup(html.text, 'lxml')
		[Event(event_soup) for event_soup in soup.find_all('div','list-card-v2 l-mar-top-2 js-d-poster')]  # pass soup to event constructor
		next_page_exists = False

class Event:
	# def print_self(self):
		# print self.__dict__

	def __init__(self, soup):
		global coll
		self.url = soup['data-share-url'].encode('UTF-8').strip() # event url

		ret = coll.find({'url' : self.url })
		if ret.count() != 0:
			return
			# print "%s: %d" % (self.url, ret.count())
			# for doc in ret:
				# print doc['title']

		try:
			self.title = soup['data-share-name'].encode('UTF-8').strip() # event title
		except:
			self.title = "N/A"
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

		try:
			self.date = soup.find('time', 'listing-hero-date')['datetime'] # event date
		except:
			self.date = "N/A"
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
			print "[ERROR] location N/A for %s" % self.title

		coll.insert_one(self.__dict__)
		# print self.__dict__
		# other details that might be worth storing: image, description

def main(argv):
	connectToDB()
	parse_eventbrite()

if __name__ == '__main__' :
	main(sys.argv[1:])
