# -*- coding:utf-8 -*-

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
		print '    webscan.py url'
		print '    webscan.py url result.txt'

	def scan_url(self,url):

		if re.match(r'^http.*',url):
			url = url.split('//')[1]

		r = requests.get('http://dns.aizhan.com/{0}/'.format(url))

		doc = pq(r.text)

		for i in doc('ul.clearfix').items():

			self.domain_info['domain'] = i('li')('strong.blue').text()
			self.domain_info['ip'] = i('li')('strong.red').text()
			self.domain_info['place'] =  i('li')('strong').eq(2).text()
			self.domain_info['number'] =  i('li')('span.red').text()

		for x in doc('.pager')('ul')('li')('a').items():

			if re.match(r'^http.*',x.attr.href):
				print '[+] Get',len(self.url_list),'urls'

				if raw_input('next?') in ['yes','y']:
					resp = requests.get(x.attr.href)
					d = pq(resp.text)

					for y in d('.table')('a').items():
						self.url_list.append(y.attr.href)
				else:
					return 0

	def scan_result(self):

		print '[*] Domain:',self.domain_info['domain']
		print '[*] IP:',self.domain_info['ip']
		print '[*] Place:',self.domain_info['place']
		print '[*] Number:',self.domain_info['number']
		print

		for u in self.url_list:

			print u

	def save_result(self,filename):

		with open(filename,'w') as f:

			f.write('Domain: '+self.domain_info['domain'])
			f.write('\n')
			f.write('IP: '+self.domain_info['ip'])
			f.write('\n')
			f.write('Place: '+self.domain_info['place'].encode('utf-8'))
			f.write('\n')
			f.write('Number: '+self.domain_info['number'])
			f.write('\n')
			f.write('\n')

			for u in self.url_list:

				f.write(u)
				f.write('\n')

		print '[*] Result saved at',os.path.join(os.path.abspath('.'),filename)

def main():

	scan = WebScan()

	if len(sys.argv) == 2:

		scan.scan_url(sys.argv[1])
		scan.scan_result()

	elif len(sys.argv) == 3:
		
		scan.scan_url(sys.argv[1])
		scan.save_result(sys.argv[2])

	else:
		scan.usage()

if __name__ == '__main__':

	main()
