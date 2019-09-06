from lxml import etree
from selenium import webdriver
import time
from sqlutils import DB


class spider_stock():
    def __init__(self):
        self.stock_current_info_url = ""
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.set_headless()
        self.browser = webdriver.Chrome(chrome_options=chromeOptions)
        self.browser.maximize_window()

    def ready_brower(self, stock_current_info_url):
        self.browser.get(stock_current_info_url)

    def turnWindow(self):
        self.browser.close()

    def create_url(self, code, industry_news_url):
        if (code[0] == '0'):
            return industry_news_url.format('sz' + code)
        elif (code[0] == '6'):
            return industry_news_url.format('sh' + code)

    def getPage(self):
        return self.browser.page_source

    def parse_stock_current_info(self, url):
        self.ready_brower(url)
        html = self.getPage()
        tree_stock_current_info = etree.HTML(html)
        # self.turnWindow()
        # 爬取股票当前价格
        stock_current_price = tree_stock_current_info.xpath("//div[@id='price']/text()")[0]
        # print("current_price: " + stock_current_price)
        # 爬取当前时间
        stock_current_time = str(tree_stock_current_info.xpath("//div[@id='hqTime']/text()")[0]).strip('\n ')
        # print("current_time: " +  stock_current_time)
        # 爬取涨停价格
        # stock_limit_up_price = tree_stock_current_info.xpath("//div[@id='ud_limie']/div[1]/text()")[0][-5:]
        # 爬取跌停价格
        # stock_limit_down_price = tree_stock_current_info.xpath("//div[@id='ud_limie']/div[2]/text()")[0][-5:]
        # print("stock_limit_up_price: " + stock_limit_up_price)
        # print("stock_limit_down_price: " + stock_limit_down_price)
        # 爬取涨跌幅
        stock_change = tree_stock_current_info.xpath("//div[@id='change']/text()")[0]
        stock_change_percentage = tree_stock_current_info.xpath("//div[@id='changeP']/text()")[0]
        print('stock_change: ' + stock_change)
        print('stock_change_percentage: ' + stock_change_percentage)
        # 爬取开盘价
        stock_opening_price = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[1]/td[1]/text()")[0]
        # print('stock_opening_price: ' + stock_opening_price)
        # 爬取成交量
        # stock_trading_volume = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[1]/td[2]/text()")[0]
        # print('VOL: ' + stock_trading_volume)
        # 爬取振幅
        # stock_amplitude = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[1]/td[3]/text()")[0]
        # print('stock_amplitude: ' + stock_amplitude)
        # 爬取当日最高价格
        stock_max_price = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[2]/td[1]/text()")[0]
        # 爬取当日成交额
        stock_trading_amount = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[2]/td[2]/text()")[0]
        # 爬取换手率
        stock_turnover_rate = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[2]/td[3]/text()")[0]
        # print('stock_max_price: ' + stock_max_price)
        # print('stock_trading_amount: ' + stock_trading_amount)
        # print('stock_turnover_rate: ' + stock_turnover_rate)
        # 爬取当日最低价格
        stock_min_price = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[3]/td[1]/text()")[0]
        # 爬取总市值
        # stock_total_market_value = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[3]/td[2]/text()")[0]
        # 爬取市净率
        # stock_PB_ratio = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[3]/td[3]/text()")[0]
        # print('stock_min_price: ' + stock_min_price)
        # print('stock_total_market_value: ' + stock_total_market_value)
        # print('stock_PB_ratio: ' + stock_PB_ratio)
        # 爬取昨日收盘价
        # stock_previous_closing_price = \
        #     tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[4]/td[1]/text()")[0]
        # 爬取流通值
        # stock_circulation_value = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[4]/td[2]/text()")[0]
        # 爬取市盈率
        # stock_PE_ratio = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[4]/td[3]/text()")[0]
        # print('stock_previous_closing_price: ' + stock_previous_closing_price)
        # print('stock_circulation_value: ' + stock_circulation_value)
        # print('stock_PE_ratio: ' + stock_PE_ratio)
        # 爬取总股本
        stock_total_equity = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[5]/td[1]/text()")[0]
        # 爬取流通值
        stock_flow_of_equity = tree_stock_current_info.xpath("//div[@id='hqDetails']//tbody/tr[5]/td[2]/text()")[0]
        # print('stock_total_equity: ' + stock_total_equity)
        # print('stock_flow_of_equity: ' + stock_flow_of_equity)
        # 流通股本占比
        stock_flow_of_equity_rate = float(stock_flow_of_equity[:4]) / float(stock_total_equity[:4])
        # "%.2f%%" % (a * 100) 可以完成小数转百分数
        # print('stock_flow_of_equity_rate: ' + str("%.2f%%" % (stock_flow_of_equity_rate * 100)))
        return stock_current_price, stock_current_time, stock_turnover_rate, stock_flow_of_equity_rate, stock_max_price, stock_min_price, stock_opening_price, stock_trading_amount, stock_change_percentage

    def closeBrower(self):
        self.browser.quit()


if __name__ == "__main__":
    count = 0
    db = DB("parse")
    ss = spider_stock()
    # 获取stock list
    results = db.getInfos("stocklist")
    sql = 'insert into stockprice (date,price,turnover,code,flow_of_equity,max_price, min_price, open_price, trading_amount, change_percentage) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    start = int(time.time())
    while count < 12:
        end = int(time.time())
        if (end - start) % 60 == 0:
            for result in results:
                code = result[1]
                print(code)
                stock_current_info_url = 'https://finance.sina.com.cn/realstock/company/{}/nc.shtml'
                stock_current_info_url = ss.create_url(code, stock_current_info_url)
                price, atime, turnover, flow_of_equity, max_price, min_price, open_price, trading_amount, change_percentage = ss.parse_stock_current_info(
                    stock_current_info_url)
                turnover = float(str(turnover).replace("%", "")) / 100.0
                print(price)
                print(atime)
                print(turnover)
                print(flow_of_equity)
                print(max_price)
                print(min_price)
                print(open_price)
                print(trading_amount)
                print(change_percentage)
                values = [atime, price, turnover, code, flow_of_equity, float(max_price), float(min_price),
                          float(open_price),
                          float(trading_amount[:-2]), change_percentage]
                print(values)
                db.insertInfo(sql, values)
            print("-----------------------")
            count += 1
    ss.closeBrower()
