# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import Column, String, create_engine, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 数据库连接信息
db_host = '********'
db_user = '********'
db_pawd = '********'
db_name = '********'
db_port = 3306

# 创建对象的基类:
Base = declarative_base()


# 定义Channel对象:
class Bili(Base):
    # 表名
    __tablename__ = 'bili'
    # 表结构
    # id = Column(Integer, unique=True, primary_key=True)
    mid = Column(Integer, unique=True, primary_key=True)
    name = Column(String(1024))
    sex = Column(String(1024))
    face = Column(String(1024))
    coins = Column(String(1024))
    spacesta = Column(String(1024))

    birthday = Column(String(1024))
    place = Column(String(1024))

    description = Column(String(1024))
    article = Column(Integer)
    following = Column(Integer)
    fans = Column(Integer)
    playnum = Column(Integer)
    sign = Column(String(1024))
    level = Column(Integer)
    exp = Column(Integer)


class BilicrawlPipeline(object):
    def __init__(self):
        pass
        # 初始化数据库连接,:
        engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
                               .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def process_item(self, item, spider):
        info = Bili(
            mid=item["mid"],
            name=item["name"],
            sex=item["sex"],
            face=item["face"],
            coins=item["coins"],
            spacesta=item["spacesta"],
            birthday=item["birthday"],
            place=item["place"],
            description=item["description"],
            article=item["article"],
            following=item["following"],
            fans=item["fans"],
            playnum=item["playnum"],
            sign=item["sign"],
            level=item["level"],
            exp=item["exp"],
        )
        self.session.add(info)
        self.session.commit()

        return item
