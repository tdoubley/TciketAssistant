#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-09 12:19:34
# @Author  : tdoubley (tdoubley@163.com)
# @Link    : http://www.cnblogs.com/TB-Go123/
# @Version : $Id$

import os

query_url_format = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=%s'

station_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8955'

def get_tickets_url(from_station, to_station, train_date, purpose_codes):
	if from_station == '' or to_station == '' or train_date == '' or purpose_codes == '':
		return None
	else:
		return query_url_format % (train_date, from_station, to_station, purpose_codes)

def get_stations_url():
	return station_url
	pass
