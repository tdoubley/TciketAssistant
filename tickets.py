#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-07 16:57:43
# @Author  : tdoubley (tdoubley@163.com)
# @Link    : http://www.cnblogs.com/TB-Go123/
# @Version : $Id$

import logging; logging.basicConfig(level=logging.INFO)
import re, time, os, certifi
import requests
from response_handler import stations_query_handler, ticket_price_query_handler, tickets_query_handler, train_no_query_handler

from url_constructor import get_stations_url, get_tickets_url

def requests_get_ssl(url):
	"""
	get with SSL
	"""
	return requests.get(url, verify=certifi.where())

def is_right_date(date):
	m = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', date)
	if m != None:
		try:
			if int(m.group(1)) > 0 and ( int(m.group(2)) > 0 and int(m.group(2)) <=12) and ( int(m.group(3)) > 0 and int(m.group(3)) <= 31):
				return True
		except:
			pass
	return False

class TciketsUtils(object):

	def __init__(self):
		self.__stations = None
		pass

	def get_station_info(self, url):
		logging.info('get stations : %s' % url)
		response = requests_get_ssl(url)
		self.__stations = stations_query_handler(response)
		if len(self.__stations) == None:
			raise RuntimeError('failed to get stations.')

	def get_query_url(self, from_station, to_station, train_date='', isAdult=True):
		from_s = self.__stations.get(from_station.encode('utf-8'), '')
		to_s = self.__stations.get(to_station.encode('utf-8'), '')
		date = train_date if is_right_date(train_date) else time.strftime("%Y-%m-%d", time.localtime())
		code = 'ADULT' if isAdult else '0x00'
		return get_tickets_url(from_s, to_s, date, code)

	def get_tickets(self, from_station, to_station, train_date='', isAdult=True):
		query_url = self.get_query_url(from_station, to_station, train_date, isAdult)
		logging.info('get tickets : %s' % query_url)
		response = requests_get_ssl(query_url)
		tickets = tickets_query_handler(response)
		return tickets


if __name__ == '__main__':
	ticket = TciketsUtils()
	ticket.get_station_info(get_stations_url())
	all = ticket.get_tickets('南京', '北京')
	print(all[1])



