# coding:utf-8
import requests
import json

from sqlalchemy import Column, String, create_engine, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 数据库连接信息
db_host = '***********'
db_user = '***********'
db_pawd = '***********'
db_name = '***********'
db_port = 3306

# 创建对象的基类:
Base = declarative_base()


# 定义Channel对象:
class Bili(Base):
    # 表名
    __tablename__ = 'bili'
    # 表结构
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


class BiliCrawl(object):
    def __init__(self):
        engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
                               .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def main(self):
        for i in range(1, 100000000):
            user_id = i
            user_url = "https://space.bilibili.com/ajax/member/GetInfo"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'http://space.bilibili.com/{}'.format(user_id),
                'Origin': 'http://space.bilibili.com',
                'Host': 'space.bilibili.com',
                'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
            }
            post_data = {
                "mid": "{}".format(user_id),
                "csrf": "null",
            }
            num = 0
            while num < 5:
                try:
                    user_response = requests.post(user_url, headers=headers, data=post_data)
                    print(user_response.json())
                    jscontent = user_response.text
                    jsDict = json.loads(jscontent)
                    statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
                    item = {}
                    if statusJson == True:
                        if 'data' in jsDict.keys():
                            jsData = jsDict['data']
                            item["mid"] = jsData['mid']
                            item["name"] = jsData['name']
                            item["sex"] = jsData['sex']
                            item["face"] = jsData['face']
                            item["coins"] = jsData['coins']
                            item["spacesta"] = jsData['spacesta']
                            item["birthday"] = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
                            item["place"] = jsData['place'] if 'place' in jsData.keys() else 'noplace'
                            item["description"] = jsData['description']
                            item["article"] = jsData['article']
                            item["playnum"] = jsData['playNum']
                            item["sign"] = jsData['sign']
                            item["level"] = jsData['level_info']['current_level']
                            item["exp"] = jsData['level_info']['current_exp']
                            item["following"] = 0
                            item["fans"] = 0

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
                    num = 10
                except Exception as e:
                    print("Error:{} mid = {}".format(e, user_id))
                    num = num + 1


if __name__ == "__main__":
    bilibili = BiliCrawl()
    bilibili.main()
