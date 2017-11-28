# -*- coding:utf-8 -*-

import socket
import requests
from pyquery import PyQuery as pq
import re
import sys
import os

class WebScan(object):

	def __init__(self):

		self.domain_info = {}
		self.url_list = []

	def usage(self):

		print '''
__        __   _    ____                  
\ \      / /__| |__/ ___|  ___ __ _ _ __  
 \ \ /\ / / _ \ '_ \___ \ / __/ _` | '_ \ 
  \ V  V /  __/ |_) |__) | (__ (_| | | | |
   \_/\_/ \___|_.__/____/ \___\__,_|_| |_|
                -- Find the same IP site
		'''
		print 'Usage:'
		print '    webscan.py <api> url'
		print '    webscan.py <api> url result.txt'
		print
		print 'APIs:'
		print '    aizhan    From dns.aizhan.com'
		print '    bing      From www.bing.com'

	def aizhan_api(self,url):

		if re.match(r'^http.*',url):
			url = url.split('//')[1]

		r = requests.get('http://dns.aizhan.com/{0}/'.format(url))
		doc = pq(r.text)

		self.domain_info['domain'] = url
		self.domain_info['ip'] = doc('ul.clearfix')('li')('strong.red').text()
		self.domain_info['place'] = doc('ul.clearfix')('li')('strong').eq(2).text()
		self.domain_info['number'] = doc('ul.clearfix')('li')('span.red').text()

		for x in doc('.pager')('ul')('li')('a').items():

			if re.match(r'^http.*',x.attr.href):
				print '[+] Get',len(self.url_list),'urls'

				if raw_input('next?') in ['yes','y']:
					resp = requests.get(x.attr.href)
					d = pq(resp.text)

					for y in d('.table')('a').items():
						self.url_list.append('http://'+y.attr.href+'/')
				else:
					return 0

	def bing_api(self,url):

		if re.match(r'^http.*',url):
			url = url.split('//')[1]

		r = requests.get('http://www.bing.com/search?q=ip:{0}'.format(socket.gethostbyname(url)))
		doc = pq(r.text)

		self.domain_info['domain'] = url
		self.domain_info['ip'] = socket.gethostbyname(url)
		self.domain_info['place'] = doc('div').filter('.b_xlText').text()
		self.domain_info['number'] = doc('span').filter('.sb_count').text()

		for x in doc('ul').filter('.sb_pagF')('li')('a').items():

			if not x.attr.href == None:
				print '[+] Get',len(self.url_list),'urls'

				if raw_input('next?') in ['yes','y']:
					resp = requests.get('http://www.bing.com/{0}'.format(x.attr.href.replace('%3a',':')))
					d = pq(resp.text)

					for y in d('cite').items():
						self.url_list.append('http://'+y.text().split('/')[0]+'/')
				else:
					return 0


	def result(self):

		print '[*] Domain:',self.domain_info['domain']
		print '[*] IP:',self.domain_info['ip']
		print '[*] Place:',self.domain_info['place']
		print '[*] Number:',self.domain_info['number']
		print

		for u in self.url_list:

			print u

	def save(self,filename):

		with open(filename,'w') as f:

			f.write('Domain: '+self.domain_info['domain'])
			f.write('\n')
			f.write('IP: '+self.domain_info['ip'])
			f.write('\n')
			f.write('Place: '+self.domain_info['place'].encode('utf-8'))
			f.write('\n')
			f.write('Number: '+self.domain_info['number'].encode('utf-8'))
			f.write('\n')
			f.write('\n')

			for u in self.url_list:

				f.write(u)
				f.write('\n')

		print '[*] Result saved at',os.path.join(os.path.abspath('.'),filename)

def main():

	scan = WebScan()

	if len(sys.argv)==3:
		if sys.argv[1] == 'aizhan':
			scan.aizhan_api(sys.argv[2])
		elif sys.argv[1] == 'bing':
			scan.bing_api(sys.argv[2])
		else:
			print 'API Error'
		scan.result()
	elif len(sys.argv)==4:
		if sys.argv[1] == 'aizhan':
			scan.aizhan_api(sys.argv[2])
		elif sys.argv[1] == 'bing':
			scan.bing_api(sys.argv[2])
		else:
			print 'API Error'
		scan.save(sys.argv[3])
	else:
		scan.usage()


if __name__ == '__main__':

	main()
