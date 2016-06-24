# -*- coding: utf-8 -*-
import json
import urllib

import scrapy
from scrapy.http.request import Request
from project23.items import AgencyItem
from project23.items import CommitItem

class AgencysSpider(scrapy.Spider):
    name = 'AgentcysSpider'
    start_urls = ['https://kyfw.12306.cn/otn/userCommon/allProvince']

    custom_settings = {
            'ITEM_PIPELINES': {
                'project23.pipelines.AgencySQLPipeline': 300,
            }
    }

    def parse(self, response):
        url = "https://kyfw.12306.cn/otn/queryAgencySellTicket/query?" 

        j = json.loads(response.body)
        for prov in j["data"]:

            params = {"province":prov["chineseName"].encode("utf-8"), "city":"", "county":""}
            s_url = url + urllib.urlencode(params)
            # 返回item才会自动交给pipelne处理
            # 这里就是发起第二次请求，并对响应回调一个函数
            yield Request(s_url, callback = self.parse_agency)

    def parse_agency(self, response):
        datas = json.loads(response.body)
        for data in datas["data"]["datas"]:
            item = AgencyItem()
            item["province"] = data["province"]
            item["city"] = data["city"]
            item["county"] = data["county"]
            item["address"] = data["address"]
            item["name"] = data["agency_name"]
            item["windows"] = data["windows_quantity"]
            item["start"] = data["start_time_am"]
            item["end"] = data["stop_time_pm"]
            # 这里返回的item先会交给AgencySQLPipeline处理
            yield item
        # 这里返回的item同样交给AgencySQLPipeline处理
        # 不过它会触发提交数据的操作
        yield CommitItem()

