# -*- coding:utf-8 -*-

import socket
import requests
from pyquery import PyQuery as pq
import re

class WebScan(object):

	def get(self,url):

		info = {}
		r = requests.get('http://ip.chinaz.com/?ip={0}'.format(socket.gethostbyname(url)))
		list = socket.gethostbyname(url).split('.')[:-1]
		list.append('0-255')
		doc = pq(r.text)

		info['ip'] = socket.gethostbyname(url)
		info['ip_segment'] = '.'.join(list)
		info['place'] = doc('span').filter('.w50-0').eq(1).text()

		return info

	def api(self,url):

		result = []
		list = []

		r = requests.get('http://www.bing.com/search?q=ip:{0}'.format(socket.gethostbyname(url)),headers={'User-Agent':'aaaa'})
		doc = pq(r.text)

		for x in doc('ul').filter('.sb_pagF')('li')('a').items():

			if not x.attr.href == None:
				resp = requests.get('http://www.bing.com/{0}'.format(x.attr.href.replace('%3a',':')),headers={'User-Agent':'aaaa'})
				d = pq(resp.text)
				
				for y in d('li').filter('.b_algo')('h2')('a').items():
					url = 'http://'+y.attr.href.split('//')[1].split('/')[0]+'/'
					if not url in list:
						list.append(url)
						result.append({'url':url,'title':y.text()})

		return result
		
	def server(self,url):
		return requests.head('http://' + url).headers['Server']