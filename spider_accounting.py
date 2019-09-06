import requests
from lxml import etree
from sqlutils import DB
import time


def parse_basic_info(url_profile):
    # 伪装头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
    }
    # 爬取公司简介
    r_profile = requests.get(url=url_profile, headers=headers)
    r_profile.encoding = 'gbk'
    tree_profile = etree.HTML(r_profile.text)
    timeXpath = "/html/body/div[1]/div[9]/div[2]/div/div[3]/table[2]/tbody/tr[1]/td[2]/text()"
    rateXpath = "/html/body/div[1]/div[9]/div[2]/div/div[3]/table[2]/tbody/tr[67]/td[2]/text()"
    try:
        info1 = tree_profile.xpath(timeXpath)[0]
        info2 = tree_profile.xpath(rateXpath)[0]
    except:
        info1 = ""
        info2 = ""
    return info1, info2


if __name__ == '__main__':
    Baseurl = "http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{}/displaytype/4.phtml"
    db = DB("parse")
    results = db.getInfos("company")
    sql = 'insert into accounting (companyId,deadline,liabilities) values (%s,%s,%s);'
    for result in results:
        url = Baseurl.format(result[1])
        if int(result[1][0]) < 6:
            continue
        print(url)
        dl, li = parse_basic_info(url)
        if dl != "" and li != "" and li != "--":
            values = [result[0], dl, li]
            db.insertInfo(sql, values)
        time.sleep(0.3)
