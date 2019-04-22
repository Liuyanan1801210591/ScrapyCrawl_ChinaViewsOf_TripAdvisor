# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field,Item


class SpotItem(scrapy.Item):
    #城市信息
    city_id=Field()         #
    city_name=Field()       #
    city_prov=Field()
    total_spot=Field()
    total_comm=Field()

    #景点表
    spot_id=Field()         #
    spot_CH_name=Field()    #
    spot_EN_name=Field()    #
    spot_rank=Field()       #
    spot_type=Field()       #
    comm_num=Field()        #
    spot_score=Field()      #
    address=Field()         #
    pic_num=Field()         #
    spot_sum=Field()        #

    #评论表
    comm_id=Field()         #
    comm_date=Field()       #
    comm_name=Field()       #
    comm_score=Field()      #
    comm_content=Field()    #
    comm_title=Field()      #
    rating_5=Field()        #
    rating_4=Field()        #
    rating_3=Field()        #
    rating_2=Field()        #
    rating_1=Field()        #

    #附近酒店表
    nearby_hotel_id=Field()     #
    nearby_hotel_name=Field()   #
    nearby_hotel_dist=Field()   #

    #附近餐厅表
    nearby_rest_id=Field()      #
    nearby_rest_name=Field()    #
    nearby_rest_dist=Field()    #

    #附近景点表
    nearby_spot_id=Field()      #
    nearby_spot_name=Field()    #
    nearby_spot_dist=Field()    #
