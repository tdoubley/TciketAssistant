#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-07 11:47:22
# @Author  : tdoubley (tdoubley@163.com)
# @Link    : http://www.cnblogs.com/TB-Go123/
# @Version : $Id$

import requests
import asyncio

from urllib import request

def get_ticket(url):
	rs = requests.get(url, verify = False)
	print(rs.text)
	#return rs

def get_station_info(url):
	pass

def getURL(src_station, dest_station):
	pass

stationURL = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8955'

get_ticket(stationURL)

url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-01-08&leftTicketDTO.from_station=NJH&leftTicketDTO.to_station=SHH&purpose_codes=ADULT'
get_ticket(url)


