#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-09 11:34:10
# @Author  : tdoubley (tdoubley@163.com)
# @Link    : http://www.cnblogs.com/TB-Go123/
# @Version : $Id$


import re, json

def parser_station(str):
	"""
	从获取站点名的response中提取[站点名-站点缩写]信息，组合成dict返回

	"var station_names ='@bjb|北京北|VAP|beijingbei|bjb|0@bjd|北京东|BOP|beijingdong|bjd|1@bji|北京|BJP|beijing|bj|2@bjn|北京南|VNP|beijingnan|bjn|3@bjx|北京西|BXP|beijingxi|bjx|4@gzn|广州南|IZQ|guangzhounan|gzn|5'"
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
	获取查询结果中每一项中的信息

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
	ret['unknow1'] = res[11]
	ret['date'] = res[12] #查询日期
	ret['unknow2'] = res[13]
	ret['unknow3'] = res[14]
	ret['price_from'] = res[15] #查询价格时的出发站点代码
	ret['price_to'] = res[16] #查询价格是的到达站点代码

	return ret

def parser_qurey_result(res):
	"""
	提取查询response中的每一火车票信息项，组合成list

	'{"data":{"flag":"1","map":{"AOH":"上海虹桥","NJH":"南京","NKH":"南京南","SHH":"上海","SNH":"上海南"},"result":["火车票信息1","火车票信息2"]},"httpstatus":200,"messages":"","status":true}
	"""
	res_format = json.loads(res)
	data = res_format.get('data', '')
	stations_map = data.get('map', '') #属于出发站点城市或目的站点城市的站点，
	trains_list = data.get('result', '') #火车票信息list

	all_info = []
	for x in trains_list:
		r = parser_train_info(x)
		all_info.append(r)

	return all_info

def tickets_query_handler(response):
	'''
	query tickets
	'''
	return parser_qurey_result(response.text)
	pass

def stations_query_handler(response):
	'''
	query stations abbreviation(缩写)
	'''
	return parser_station(response.text)
	pass

def train_no_query_handler(response):
	'''
	query train_no
	'''
	pass

def ticket_price_query_handler(response):
	'''
	query tickets price
	'''
	pass

