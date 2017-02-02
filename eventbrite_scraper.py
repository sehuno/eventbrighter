#!/bin/python
import os
import re
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
