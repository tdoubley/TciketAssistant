# 12306火车票信息查询工具



## 一、预期目标

- [ ] 查指定日期的出发站点和额目标站点的火车票（包括票价等信息）
- [ ] 查指定型号车型的站点及到站时间等情况





## 二、12306 API

### 1. 获取站点缩写:

* url

  >1. **station_version:** 版本
  >
  >```python
  >url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8968'
  >```

* response 

  > 1. **格式:** `@+bjb+北京北+VAP+beijingbei+bjb+0` ， `@`开始以`|`分割
  >
  > ```python
  > response = "var station_names ='@bjb|北京北|VAP|beijingbei|bjb|0@bjd|北京东|BOP|beijingdong|bjd|1@bji|北京|BJP|beijing|bj|2@bjn|北京南|VNP|beijingnan|bjn|3@bjx|北京西|BXP|beijingxi|bjx|4@gzn|广州南|IZQ|guangzhounan|gzn|5'"
  > ```

### 2. 获取火车编号`train_no`

* url

  > 1. **scriptVersion:** 版本
  >
  > ```python
  > url = 'https://kyfw.12306.cn/otn/resources/js/query/train_list.js?scriptVersion=1.5462'
  > ```

* response

  > 1. **station_train_code:** 车次名称+起始站点
  > 2. **train_no：** 唯一编码
  >
  > ```python
  > url = "var train_list ={"2018-01-31":{},"2018-01-30":{},"2018-03-01":{},"2018-03-03":{},"2018-03-02":{},"2018-03-05":{},"2018-03-04":{},"2018-03-07":{},"2018-03-06":{},"2018-03-09":{},"2018-03-08":{},"2018-03-16":{},"2018-03-15":{},"2018-03-14":{},"2018-03-13":{},"2017-12-31":{"D":[{"station_train_code":"D1(北京-沈阳)","train_no":"24000000D10V"},{"station_train_code":"D2(沈阳-北京)","train_no":"12000000D20J"},{"station_train_code":"D3(北京-沈阳北)","train_no":"24000000D30Q"},{"station_train_code":"D4(沈阳北-北京)","train_no":"12000000D40E"},{"station_train_code":"D6(沈阳北-北京)","train_no":"12000000D60G"}],"Z":[{"station_train_code":"Z1(北京西-长沙)","train_no":"24000000Z10C"},{"station_train_code":"Z2(长沙-北京西)","train_no":"62000000Z201"},{"station_train_code":"Z3(北京西-重庆北)","train_no":"24000000Z30I"},{"station_train_code":"Z4(重庆北-北京西)"}]}}"
  > ```

### 3. 获取火车票信息

* url

  > - **train_date:** 查询的时间
  > - **from_station：** 出发站点
  > - **to_station:** 目的站点
  > - **purpose_codes:** 成人票（`ADULT`）或学生票（`0x00`）
  >
  > ```python
  > url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-01-07&leftTicketDTO.from_station=NJH&leftTicketDTO.to_station=SHH&purpose_codes=ADULT'
  > ```

* response

  > 1.  **flag:** 查询的时间
  >
  >
  > 2. **map：** 出发站点
  > 3. **result:** 目的站点
  > 4. **httpstatus:** 成人票（`ADULT`）或学生票（`0x00`）
  > 5. **messages**: 
  > 6. **status:**
  >
  > ```
  > response = '{"data":{"flag":"1","map":{"AOH":"上海虹桥","NJH":"南京","NKH":"南京南","SHH":"上海","SNH":"上海南"},"result":["R%2FU5fJP%2FaKGB0pbO5JdQK%2FnDRLIe%2B0Ubk0wUlnya2D6igMnHe%2FrD3fBoeb1h%2FpKqhFgGTKC62eCo%0ABl5ScEtgXGrBe12La6wQhaS2WMSKGY09HK%2FkCMS4oMt1z%2B8YShQZrjPEmv8Gj13Ssuj%2BcvRnI6mF%0AtvJWcc64pBThmjDYlHt4%2FgizdsbnOdwuhqQSbpojTBHb1v9%2FXSnSBjFUCikT%2FEmQjdKlzuSLyoHk%0Ax%2ByFQfXofqK1f6xTmigMWYyvSPfmm8nWo4kPH2I%3D|预订|47000K151103|K1511|UCK|YWH|NJH|SNH|00:46|04:21|03:35|Y|BRTyqDOj%2BFnfxsQR6vQWwztBFpbEUcSFf6YqBJ%2FiS3HVCgJl%2Bar%2FSXKEOrE%3D|20180108|3|KA|13|17|0|0||||10|||有||8|有|||||10401030|1413|0","AKlqBFzH5Mos9dKUVvwuAlW7wRI3QBvyfK3sQVfoUuB%2B9dEBApC459kEIa3HoDnE6lkC4J2jRykz%0AMOpyyYxvnqVurTDoPN4jlMW4yJMiViDScVsjexbAM0L26j6cjLj5fxHsH5MiQzeyj0Za3WZrXd03%0AZAlpiiS4T0jZk6Z6efbCRVzuepRYEszOGJllxEXEvV9CpvZgN8WBdRfg7ZoduZjNe3jHb7H7u8sQ%0A7CgkQbjGRYV6SW0EXi0jasm3FBXx|预订|48000K835401|K8351|UKH|HZH|NJH|SNH|00:52|05:36|04:44|Y|D7QJAjbktUT79wcEtzy72NyAwctRO6Sfrd%2Bl5y2i2%2FEg5Vo9|20180108|3|H3|09|11|0|0|||||||有||有|有|||||101030|113|0"]},"httpstatus":200,"messages":"","status":true}
  > ```

### 4. 获取票价

- url

  > - **train_no:** 火车编号
  > - **from_station：** 出发站点的编号（可以从查询火车票信息的response中获取）
  > - **to_station:** 目的站点的编号
  > - **purpose_codes:** 成人票（`ADULT`）或学生票（`0x00`）
  >
  > ```python
  > url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no=380000K1540D&from_station_no=08&to_station_no=10&seat_types=1413&train_date=2018-02-05'
  > ```

- response

  > 1. **train_date:** 查询的时间
  >
  > 2. **类别**：
  >
  >    > A9:特等座
  >    > M:一等座
  >    > O:二等座
  >    > A6:高级软卧
  >    > A4:软卧
  >    > A3:硬卧
  >    > A2:软座
  >    > A1:硬座
  >    > WZ:无座
  >    > F:动卧
  >
  > 3. ​
  >
  > ```python
  > response = '{"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"3":"925","A1":"¥46.5","1":"465","A4":"¥140.5","A3":"¥92.5","4":"1405","OT":[],"WZ":"¥46.5","train_no":"380000K1540D"},"messages":[],"validateMessages":{}}'
  > ```
  >

### ##二、

