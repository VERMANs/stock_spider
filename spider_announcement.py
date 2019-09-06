# 获得指定公司的报告
# 大新闻 （无需时刻请求）

import requests
from lxml import etree
from sqlutils import DB


def parse_company_announcement(announcement_url):
    # 伪装头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
    }
    # 访问公告页
    r_announcement = requests.get(url=announcement_url, headers=headers)
    r_announcement.encoding = 'gbk'
    tree_announcement = etree.HTML(r_announcement.text)
    # 爬取公告日期、名称和内容
    announcement_date = tree_announcement.xpath("//div[@class='datelist']/ul/text()")
    for i in range(len(announcement_date)):
        announcement_date[i] = str(announcement_date[i]).strip('\t\t\t\r\n\xa0')
    announcement_date.pop()  # 不知道什么原因，这个表里面多一个空的元素
    # 爬取公告名称
    announcement_name = tree_announcement.xpath("//div[@class='datelist']/ul/a/text()")
    # 爬取公告链接
    announcement_link = tree_announcement.xpath("//div[@class='datelist']/ul/a/@href")
    for i in range(len(announcement_link)):
        # 构造url
        announcement_link[i] = 'http://vip.stock.finance.sina.com.cn' + announcement_link[i]
        # 访问二级页面
        r_announcement_i = requests.get(url=announcement_link[i], headers=headers)
        r_announcement_i.encoding = 'gbk'
        tree_announcement_i = etree.HTML(r_announcement_i.text)
        # 爬取公告文件url
        announcement_i_url = tree_announcement_i.xpath("//table[@id='allbulletin']//font[@size='2']/a/@href")[0]
        announcement_link[i] = announcement_i_url

    # print(len(announcement_name))
    # print(len(announcement_date))
    # print(len(announcement_link))
    # for i in range(len(announcement_name)):
    #     print(announcement_date[i])
    #     print(announcement_link[i])
    return announcement_name, announcement_date, announcement_link


def getCompanyAnnounceInfo(code):
    announcement_url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/{}.phtml'
    announcement_url = announcement_url.format(code)
    return parse_company_announcement(announcement_url)


if __name__ == "__main__":
    db = DB("parse")
    codelists = ["600116", "600132", "600292"]
    ids = ["104", "119", "139"]
    sqlString = 'insert into announcement (companyId,date,url,name) values (%s,%s,%s,%s);'
    for i in range(len(codelists)):
        announcement_name, announcement_date, announcement_link = getCompanyAnnounceInfo(codelists[i])
        id = ids[i]
        for i in range(len(announcement_name)):
            name = announcement_name[i]
            date = announcement_date[i]
            link = announcement_link[i]
            values = [id, date, link, name]
            db.insertInfo(sqlString, values)
    db.closeDB()
