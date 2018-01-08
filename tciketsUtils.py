#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-07 16:57:43
# @Author  : tdoubley (tdoubley@163.com)
# @Link    : http://www.cnblogs.com/TB-Go123/
# @Version : $Id$

import logging; logging.basicConfig(level=logging.INFO)
import re, json, time, os, certifi
import requests

url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-01-07&leftTicketDTO.from_station=NJH&leftTicketDTO.to_station=SHH&purpose_codes=ADULT'

url_format = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=%s'

stationURL = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8955'


def parser_station(str):
	"""
	var station_names ='@bjb|北京北|VAP|beijingbei|bjb|0@bjd|北京东|BOP|beijingdong|bjd|1@bji|北京|BJP|beijing|bj|2@bjn|北京南|VNP|beijingnan|bjn|3@bjx|北京西|BXP|beijingxi|bjx|4@gzn|广州南|IZQ|guangzhounan|gzn|5'

	@+bjb+北京北+VAP+beijingbei+bjb+0
	"""
	stations_str = re.split(r'\=', str)[1]
	stations = dict()
	stations_info = [x for x in re.split('\@|\'|\;', stations_str) if x != '']
	for x in stations_info:
		station = x.split('|')
		if len(station) > 3:
			stations[station[1].encode('utf-8')] = station[2]
	if len(stations) == 0:
		return None
	return stations

def parser_train_info(info):
	"""
	"R%2FU5fJP%2FaKGB0pbO5JdQK%2FnDRLIe%2B0Ubk0wUlnya2D6igMnHe%2FrD3fBoeb1h%2FpKqhFgGTKC62eCo%0ABl5ScEtgXGrBe12La6wQhaS2WMSKGY09HK%2FkCMS4oMt1z%2B8YShQZrjPEmv8Gj13Ssuj%2BcvRnI6mF%0AtvJWcc64pBThmjDYlHt4%2FgizdsbnOdwuhqQSbpojTBHb1v9%2FXSnSBjFUCikT%2FEmQjdKlzuSLyoHk%0Ax%2ByFQfXofqK1f6xTmigMWYyvSPfmm8nWo4kPH2I%3D|预订|47000K151103|K1511|UCK|YWH|NJH|SNH|00:46|04:21|03:35|Y|BRTyqDOj%2BFnfxsQR6vQWwztBFpbEUcSFf6YqBJ%2FiS3HVCgJl%2Bar%2FSXKEOrE%3D|20180108|3|KA|13|17|0|0||||10|||有||8|有|||||10401030|1413|0"

	['预订', '850000Z21841', 'Z215', 'LZJ', 'SHH', 'NJH', 'SHH', '12:23', '14:54', '02:31', 'Y', 'I2QdujqbL2PyuXTM%2B1uCdIzZbNvZ1dQMVJ3R6AiDvEqbuhQUowopJcfbVHWxk8it1HCApAAvCOo%3D', '20180107', '3', 'J1', '14', '17', '0', '0', '', '', '', '有', '2', '', '有', '', '有', '无', '', '', '', '', '1040102030', '14123', '0']
	"""
	ret = dict()
	res = info.split('|')[1:]

	#print(res)
	ret['ticket_state'] = res[0] #票的操作状态,在预定按钮上的显示内容， [预定，列车运行图调整,暂停发售,暂售至<br/>01月15日]
	ret['train_no'] = res[1] #火车的编号唯一 47000K151103
	ret['train_name'] = res[2] #火车的名字 K1511
	ret['train_stations'] = res[3:7] #始发站,终点站,起始站,目的站
	ret['departure_time'] = res[7] #出发时间
	ret['arrived_time'] = res[8] #到达时间
	ret['time_length'] = res[9] #时长
	ret['arrive_in_day'] = True if res[10] == 'Y' else False #是否当天可达

	return ret

def parser_qurey_result(res):
	"""
	{"data":{"flag":"1","map":{"AOH":"上海虹桥","NJH":"南京","NKH":"南京南","SHH":"上海","SNH":"上海南"},"result":["R%2FU5fJP%2FaKGB0pbO5JdQK%2FnDRLIe%2B0Ubk0wUlnya2D6igMnHe%2FrD3fBoeb1h%2FpKqhFgGTKC62eCo%0ABl5ScEtgXGrBe12La6wQhaS2WMSKGY09HK%2FkCMS4oMt1z%2B8YShQZrjPEmv8Gj13Ssuj%2BcvRnI6mF%0AtvJWcc64pBThmjDYlHt4%2FgizdsbnOdwuhqQSbpojTBHb1v9%2FXSnSBjFUCikT%2FEmQjdKlzuSLyoHk%0Ax%2ByFQfXofqK1f6xTmigMWYyvSPfmm8nWo4kPH2I%3D|预订|47000K151103|K1511|UCK|YWH|NJH|SNH|00:46|04:21|03:35|Y|BRTyqDOj%2BFnfxsQR6vQWwztBFpbEUcSFf6YqBJ%2FiS3HVCgJl%2Bar%2FSXKEOrE%3D|20180108|3|KA|13|17|0|0||||10|||有||8|有|||||10401030|1413|0","AKlqBFzH5Mos9dKUVvwuAlW7wRI3QBvyfK3sQVfoUuB%2B9dEBApC459kEIa3HoDnE6lkC4J2jRykz%0AMOpyyYxvnqVurTDoPN4jlMW4yJMiViDScVsjexbAM0L26j6cjLj5fxHsH5MiQzeyj0Za3WZrXd03%0AZAlpiiS4T0jZk6Z6efbCRVzuepRYEszOGJllxEXEvV9CpvZgN8WBdRfg7ZoduZjNe3jHb7H7u8sQ%0A7CgkQbjGRYV6SW0EXi0jasm3FBXx|预订|48000K835401|K8351|UKH|HZH|NJH|SNH|00:52|05:36|04:44|Y|D7QJAjbktUT79wcEtzy72NyAwctRO6Sfrd%2Bl5y2i2%2FEg5Vo9|20180108|3|H3|09|11|0|0|||||||有||有|有|||||101030|113|0"]},"httpstatus":200,"messages":"","status":true}
	"""

	res_info = json.loads(res)
	stations_info = res_info['data']['map'] #属于出发站点城市或目的站点城市的站点，
	trains_info = res_info['data']['result']

	all_info = []
	for x in trains_info:
		r = parser_train_info(x)
		all_info.append(r)

	return all_info

def requests_get_ssl(url):
	return requests.get(url, verify=certifi.where())

class TciketsUtils(object):

	def __init__(self):
		self.__stations = None
		pass

	def get_station_info(self, url):
		reponse = requests_get_ssl(url)
		#response = "var station_names ='@bjb|北京北|VAP|beijingbei|bjb|0@bjd|北京东|BOP|beijingdong|bjd|1@bji|北京|BJP|beijing|bj|2@bjn|北京南|VNP|beijingnan|bjn|3@bjx|北京西|BXP|beijingxi|bjx|4@gzn|广州南|IZQ|guangzhounan|gzn|5'"
		self.__stations = parser_station(reponse.text)
		if len(self.__stations) == None:
			raise RuntimeError('failed to get stations.')

	def get_query_url(self, from_station, to_station, train_date='', isAdult=True):
		from_s = self.__stations.get(from_station.encode('utf-8', ''))
		to_s = self.__stations.get(to_station.encode('utf-8', ''))
		if train_date == '':
			train_date = time.strftime("%Y-%m-%d", time.localtime())
		purpose_codes = 'ADULT' if isAdult else '0x00'
		if from_s == '' or to_s == '' or train_date == '' or purpose_codes == '':
			return None
		else:
			return url_format % (train_date, from_s, to_s, purpose_codes)

	def get_tickets(self, from_station, to_station, train_date='', isAdult=True):
		query_url = self.get_query_url(from_station, to_station, train_date, isAdult)
		logging.info(query_url)
		response = requests_get_ssl(query_url)
		tickets = parser_qurey_result(response.text)
		return tickets


if __name__ == '__main__':
	#str = "var station_names ='@bjb|北京北|VAP|beijingbei|bjb|0@bjd|北京东|BOP|beijingdong|bjd|1@bji|北京|BJP|beijing|bj|2@bjn|北京南|VNP|beijingnan|bjn|3@bjx|北京西|BXP|beijingxi|bjx|4@gzn|广州南|IZQ|guangzhounan|gzn|5';"
	#print(parser_station(str))
	ticket = TciketsUtils()
	ticket.get_station_info(stationURL)
	all = ticket.get_tickets('南京', '北京')
	print(all)



