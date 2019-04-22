# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from spot_crawl.items import SpotItem
from scrapy.loader.processors import MapCompose,Join
from urllib.parse import urljoin
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
import re

class BasicSpider(CrawlSpider):
    name = 'basic'
    start_urls = ['https://www.tripadvisor.cn/Tourism-g294211-China-Vacations.html']
    download_delay = 0.5

    def spot_parse(self,response):
        l=ItemLoader(item=SpotItem(),response=response)

        '''
        城市信息
        '''

        # 城市id
        try:
            l.add_xpath('city_id', '//div[@class="global-nav-geopill"]/@data-id')
        except:
            pass

        # 城市名称
        try:
            l.add_xpath('city_name', '//div[@class="global-nav-geopill"]/span//text()')
        except:
            pass

        '''
        景点信息
        '''
        # 景点id
        try:
            l.add_xpath('spot_id', '//div[@class="blRow  showBizHour "]/attribute::data-locid')
        except:
            pass

        #景点中文名称
        try:
            l.add_xpath('spot_CH_name','//h1[@id="HEADING"]/text()')
        except:
            pass

        #景点英文名称
        try:
            l.add_xpath('spot_EN_name','//h1[@id="HEADING"]/div/text()')
        except:
            pass

        #景点排名
        try:
            l.add_xpath('spot_rank','//span[@class="header_popularity popIndexValidation  "]//span//text()')
        except:
            pass

        #景点类型
        try:
            l.add_xpath('spot_type','string(//span[@class="is-hidden-mobile header_detail attractionCategories"])')
        except:
            pass

        # 点评数量
        try:
            l.add_xpath('comm_num', '//span[@class="reviews_header_count"]/text()',
                        MapCompose(int), re='[.0-9]+')
        except:
            pass

        # 景点评分
        try:
            l.add_xpath('spot_score','//span[@class="overallRating"]/text()')
        except:
            pass

        # 地址，用string()提取子标签所有文本内容
        try:
            l.add_xpath('address', 'string(//span[@class="detail "])')
        except:
            pass

        #图片数量
        try:
            l.add_xpath('pic_num','(//*[@class="details"])[1]/text()',
                        MapCompose(int),re='[.0-9]+')
        except:
            pass

        #景点简介
        try:
            l.add_xpath('spot_sum',
                        '(//div[@class="attractions-attraction-detail-about-card-AttractionDetailAboutCard__section--1_Efg"])[1]/span/text()')
        except:
            pass

        # 5分评价数
        try:
            l.add_xpath('rating_5',
                        '(//span[text()="\u975e\u5e38\u597d"])[1]//following-sibling::span[@class="row_count row_cell"]/text()')
        except:
            pass

        # 4分评价数
        try:
            l.add_xpath('rating_4',
                       '(//span[text()="\u8f83\u597d"])[1]//following-sibling::span[@class="row_count row_cell"]/text()')
        except:
            pass

        # 3分评价数
        try:
            l.add_xpath('rating_3',
                        '(//span[text()="\u4e00\u822c"])[1]//following-sibling::span[@class="row_count row_cell"]/text()')
        except:
            pass

        # 2分评价数：
        try:
            l.add_xpath('rating_2',
                        '(//span[text()="\u8f83\u5dee"])[1]//following-sibling::span[@class="row_count row_cell"]/text()')
        except:
            pass

        # 1分评价数：
        try:
            l.add_xpath('rating_1',
                        '(//span[text()="\u5f88\u5dee"])[1]//following-sibling::span[@class="row_count row_cell"]/text()')
        except:
            pass

        '''
        评论信息
        '''
        #评论id
        try:
            l.add_xpath('comm_id','//div[@class="reviewSelector"]/attribute::data-reviewid')
        except:
            pass

        #评论人名称
        try:
            l.add_xpath('comm_name','//div[@class="info_text"]/div/text()')
        except:
            pass

        #评论标题
        try:
            l.add_xpath('comm_title','//span[@class="noQuotes"]/text()')
        except:
            pass

        #评论时间
        try:
            l.add_xpath('comm_date','//span[@class="ratingDate"]/attribute::title')
        except:
            pass

        #评价分数
        try:
            comm_score=response.xpath('//div[@class="rev_wrap ui_columns is-multiline "]//span[starts-with(@class,"ui_bubble_rating")]//attribute::class').extract()
            for i in range(len(comm_score)):
                comm_score[i]=float(re.sub("\D", "", comm_score[i]))/10.0
        except:
            pass
        else:
            l.add_value('comm_score',comm_score)

        #评论内容
        try:
            l.add_xpath('comm_content','//div[@class="ui_column is-9"]/div[@class="prw_rup prw_reviews_text_summary_hsx"]//text()')
        except:
            pass

        '''
        附近信息
        '''
        #附近酒店id
        l.add_xpath('nearby_hotel_id',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[1]//div[@class="ui_columns is-gapless is-mobile poiEntry shownOnMap"]/attribute::data-locid')

        #附近酒店名称
        l.add_xpath('nearby_hotel_name',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[1]//div[@class="ui_columns is-gapless is-mobile poiEntry shownOnMap"]/attribute::data-name')

        #附近酒店距离
        l.add_xpath('nearby_hotel_dist',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[1]//div[@class="distance"]/text()')

        # 附近餐厅id
        l.add_xpath('nearby_rest_id',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[2]//div[@class="ui_columns is-gapless is-mobile poiEntry shownOnMap"]/attribute::data-locid')

        # 附近餐厅名称
        l.add_xpath('nearby_rest_name',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[2]//div[@class="ui_columns is-gapless is-mobile poiEntry shownOnMap"]/attribute::data-name')

        # 附近餐厅距离
        l.add_xpath('nearby_rest_dist',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[2]//div[@class="distance"]/text()')

        # 附近景点id
        l.add_xpath('nearby_spot_id',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[3]//div[@class="ui_columns is-gapless is-mobile poiEntry shownOnMap"]/attribute::data-locid')

        # 附近景点名称
        l.add_xpath('nearby_spot_name',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[3]//div[@class="ui_columns is-gapless is-mobile poiEntry shownOnMap"]/attribute::data-name')

        # 附近景点距离
        l.add_xpath('nearby_spot_dist',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[3]//div[@class="distance"]/text()')

        yield l.load_item()

    #抓取景点页面
    def item_parse(self,response):
        spot_selector=response.xpath('//div[@class="listing_title "]/a/@href')
        for url in spot_selector.extract():
            yield Request(urljoin('https://www.tripadvisor.cn',url),callback=self.spot_parse)

        next_selector = response.xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]/@href')
        for url in next_selector.extract():
            yield Request(urljoin('https://www.tripadvisor.cn', url),callback=self.item_parse)


    #从城市vocation变成城市attraction页面
    def city_parse(self,response):
        #xpath返回的是列表需要提取第一项
        city_page=(response.xpath('//li[@class="attractions twoLines"]/a/@href').extract())[0]
        yield Request(urljoin('https://www.tripadvisor.cn',city_page),callback=self.item_parse)

    #动态抓取城市页面
    def parse(self, response):
        page_selector =[]
        #爬取前十页的城市，拼接爬虫地址
        for i in range(10):
            page_selector.append('https://www.tripadvisor.cn/TourismChildrenAjax?geo=294211&offset='+str(i)+'&desktop=true')
        for url in page_selector:
            yield Request(url)

        city_selector=response.xpath('//a[@class="popularCity hoverHighlight"]/@href')
        for url in city_selector.extract():
            yield Request(urljoin('https://www.tripadvisor.cn',url),callback=self.city_parse)
