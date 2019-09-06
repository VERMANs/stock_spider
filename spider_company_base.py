#  指定 code 获得公司基础信息
#  getCompanyInfo(code)

import requests
from lxml import etree
from stocks_name_and_code import parse_and_convert, search_a_company, parse_stocks_name_and_code
from sqlutils import DB
import time


# 拼接url
def modify_url(code, url_profile, url_industry):
    url_profile = url_profile.format(code)
    url_industry = url_industry.format(code)
    return url_profile, url_industry


# parse
def parse_basic_info(url_profile, url_industry):
    # 伪装头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
    }
    # 爬取公司简介
    r_profile = requests.get(url=url_profile, headers=headers)
    r_profile.encoding = 'gbk'
    tree_profile = etree.HTML(r_profile.text)
    # 公司网址
    website = tree_profile.xpath("//table[@id='comInfo1']//tr[13]//a/text()")[0]
    # 公司简介
    profile = tree_profile.xpath("//table[@id='comInfo1']//tr[20]/td[2]/text()")[0]
    # 经营范围
    operating_range = tree_profile.xpath("//table[@id='comInfo1']//tr[21]/td[2]/text()")[0]
    # # deadtime
    deadtime = str(tree_profile.xpath("//div[@id='hqTime']/text()")[0]).strip('\n ')
    # 爬取所属行业及行业内企业名单
    r_industry = requests.get(url=url_industry, headers=headers)
    r_industry.encoding = 'gbk'
    tree_industry = etree.HTML(r_industry.text)
    # 所属行业
    industry = tree_industry.xpath("//table[@class='comInfo1']//tr[3]/td[1]/text()")[0]
    # 行业内其他企业名单url
    other_companies_url = 'http://vip.stock.finance.sina.com.cn' + \
                          tree_industry.xpath("//table[@class='comInfo1']//tr[3]/td[2]/a/@href")[0]
    # 爬取这个名单
    # r_other_companies = requests.get(url=other_companies_url, headers=headers)
    # r_other_companies.encoding = 'gbk'
    # tree_other_companies = etree.HTML(r_other_companies.text)
    # other_companies_code = tree_other_companies.xpath("//table[@id='CirculateShareholderTable']//tr/td[4]/div/text()")
    # other_companies_name = []
    # for item in other_companies_code:
    #     other_companies_name.append(parse_and_convert(item))
    # print(website)  # web
    # print(profile)  # 简介
    # print(operating_range)  # 运营领域
    # print(industry)  # 公司类型
    # print(other_companies_name) #
    return industry, operating_range


def getCompanyBaseInfo(code):
    # 公司简介url
    url_profile = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/{}.phtml"
    # 所属行业url
    url_industry = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpOtherInfo/stockid/{}/menu_num/2.phtml"
    # 拼接url
    url_profile, url_industry = modify_url(code, url_profile, url_industry)
    # parse
    # print(url_profile)
    # print(url_industry)
    names, codes = parse_stocks_name_and_code()
    company = search_a_company(code, names, codes)
    industry, operating_range = parse_basic_info(url_profile, url_industry)
    return company, industry, operating_range


# if __name__ == "__main__":
#     db = DB("parse")
#     results = db.getInfos("stocklist")
#     sqlString = 'insert into company (code,industry,business,name) values (%s,%s,%s,%s);'
#     for result in results:
#         if int(result[1][0]) < 6:
#             continue
#         print(result[1])
#         try:
#             company, industry, operating_range = getCompanyBaseInfo(result[1])
#         except:
#             continue
#         values = [result[1], industry, operating_range, company]
#         db.insertInfo(sql=sqlString, values=values)
#         time.sleep(0.3)
#     db.closeDB()

if __name__ == '__main__':
    db = DB("parse")
    results = db.getInfos("stocklist")
    sqlString = 'insert into company (code,industry,business,name) values (%s,%s,%s,%s);'
    for result in results:
        if result[1] != "600292":
            continue
        print(result[1])
        try:
            company, industry, operating_range = getCompanyBaseInfo(result[1])
        except:
            continue
        values = [result[1], industry, operating_range, company]
        db.insertInfo(sql=sqlString, values=values)
        # time.sleep(0.3)
    db.closeDB()
