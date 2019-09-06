import requests
from lxml import etree
from sqlutils import DB


def parse_basic_info(url_profile, basexpath, db):
    # 伪装头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
    }
    # 爬取公司简介
    r_profile = requests.get(url=url_profile, headers=headers)
    r_profile.encoding = 'gbk'
    tree_profile = etree.HTML(r_profile.text)
    # 公司网址]
    sql = "insert into stocklist (code,name) values (%s,%s);"
    for i in range(1909):
        info = tree_profile.xpath(basexpath.format(str(i + 1)))[0]
        info = info[:-1]
        infos = str(info).split("(")
        values = [infos[1], infos[0]]
        db.insertInfo(sql, values)


if __name__ == '__main__':
    baseXpath = "/html/body/div[9]/div[2]/div/ul[1]/li[{}]/a/text()"
    max = 1909
    url = "http://quote.eastmoney.com/stock_list.html"
    db = DB("parse")
    parse_basic_info(url, baseXpath, db)
    db.closeDB()
