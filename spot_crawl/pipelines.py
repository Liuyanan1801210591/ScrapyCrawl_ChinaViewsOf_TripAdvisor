import codecs
import json

#文件json格式保存
class JsonWithEncoding(object):

    def __init__(self):
        #使用codecs模块的打开方式，可以指定编码打开，避免很多编码问题
        self.file = codecs.open("test.json","w",encoding="utf-8")

    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False)+","+"\n"
        self.file.write(lines)
        #注意别忘返回Item给下一个管道
        return item

    def spider_closed(self,spider):
        self.file.close()

import pymysql.cursors
import logging


class MySQLPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='spot',  # 数据库名
            user='root',  # 数据库用户名
            passwd='password',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();

    def process_item(self, item, spider):
        self.cursor.execute(
            """insert into test1(city_id, city_name, spot_id, spot_CH ,spot_EN, spot_rank,spot_type,comm_num,spot_score,address,pic_num,spot_sum,comm_id,comm_date,comm_name,comm_score,comm_content,comm_title,rating_5,rating_4,rating_3,rating_2,rating_1,nearby_hotel_id,nearby_hotel_name,nearby_hotel_dist,nearby_rest_id,nearby_rest_name,nearby_rest_dist,nearby_spot_id,nearby_spot_name,nearby_spot_dist)
            value (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s,%s)""",  # 纯属python操作mysql知识，不熟悉请恶补
            (item['city_id'],  # item里面定义的字段和表字段对应
             item['city_name'],
             item['spot_id'],
             item['spot_CH_name'],
             item['spot_EN_name'],
             item['spot_rank'],
             item['spot_type'],  # item里面定义的字段和表字段对应
             item['comm_num'],
             item['spot_score'],
             item['address'],
             item['pic_num'],
             item['spot_sum'],
             item['comm_id'],  # item里面定义的字段和表字段对应
             item['comm_date'],
             item['comm_name'],
             item['comm_score'],
             item['comm_content'],
             item['comm_title'],
             item['rating_5'],  # item里面定义的字段和表字段对应
             item['rating_4'],
             item['rating_3'],
             item['rating_2'],
             item['rating_1'],
             item['nearby_hotel_id'],
             item['nearby_hotel_name'],
             item['nearby_hotel_dist'],
             item['nearby_rest_id'],
             item['nearby_rest_name'],
             item['nearby_rest_dist'],
             item['nearby_spot_id'],
             item['nearby_spot_name'],
             item['nearby_spot_dist']
             ))

        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回