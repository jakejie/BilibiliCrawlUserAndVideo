import threading
import time
from concurrent import futures

# import pymysql
import requests
# coding:utf-8
import requests
import json

from sqlalchemy import Column, String, create_engine, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

# 数据库连接信息
db_host = '********'
db_user = '********'
db_pawd = '********'
db_name = '********'
db_port = 3306

# 创建对象的基类:
Base = declarative_base()

total = 1
result = []
lock = threading.Lock()


# 定义Channel对象:
class BiliVideo(Base):
    # 表名
    __tablename__ = 'bilivideo'
    aid = Column(Integer, unique=True, primary_key=True)  # 视频编号
    view = Column(Integer)  # 播放量
    danmaku = Column(Integer)  # 弹幕数
    reply = Column(Integer)  # 评论数
    favorite = Column(Integer)  # 收藏数
    coin = Column(Integer)  # 硬币数
    share = Column(Integer)  # 分享数
    name = Column(String(256))  # 视频名称


class Crawl(object):
    def __init__(self):
        pass
        # 初始化数据库连接,:
        engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
                               .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def main(self, url):
        # 启动爬虫
        global total
        req = requests.get(url, headers=headers, timeout=6).json()
        print(req)
        time.sleep(0.5)
        try:
            data = req['data']
            if data['view'] != "--" and data['aid'] != 0:
                video = BiliVideo(
                    aid=data['aid'],  # 视频编号
                    view=data['view'],  # 播放量
                    danmaku=data['danmaku'],  # 弹幕数
                    reply=data['reply'],  # 评论数
                    favorite=data['favorite'],  # 收藏数
                    coin=data['coin'],  # 硬币数
                    share=data['share'],  # 分享数
                    # ""  # 视频名称（暂时为空）
                )
                try:
                    self.session.add(video)
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    print("Session Error:{} URL = {}".format(e, url))
                with lock:
                    result.append(video)
                    if total % 100 == 0:
                        print(total)
                    total += 1
        except Exception as e:
            print("Error:{} URL = {}".format(e, url))


if __name__ == "__main__":
    # engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
    #                        .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
    # Base.metadata.create_all(engine)

    bili = Crawl()
    print("启动爬虫，开始爬取数据")
    for i in range(1, 2015):
        begin = 10000 * i
        urls = ["http://api.bilibili.com/archive_stat/stat?aid={}".format(j)
                for j in range(begin, begin + 10000)]
        with futures.ThreadPoolExecutor(64) as executor:
            executor.map(bili.main, urls)
    print("爬虫结束，共为您爬取到 {} 条数据".format(total))
