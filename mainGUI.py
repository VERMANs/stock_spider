import PySimpleGUI as sg
from sqlutils import DB
from GUItest import getImage
from spider_company_base import getCompanyBaseInfo
from spider_announcement import getCompanyAnnounceInfo
from spider_accounting import parse_basic_info
from spider_current_info import spider_stock

sp = spider_stock()
db = DB("parse")
results = db.getInfos("stocklist")
concernedList = (results[0][1], results[1][1], results[2][1])
baseinfo = "请刷新code信息..."
newsinfo = "请刷新code信息..."
accountinfo = "请刷新code信息..."
nowPrice = "请刷新code信息"
lastPrice = "请刷新code信息"
mainGUI = sg.Window('股票小助手')

column1 = [[sg.Text('Column 1', background_color='#d3dfda', justification='center', size=(10, 1))],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]
layout = [
    [sg.Text('         Start your Parse Spider!', size=(30, 1), font=("Helvetica", 25))],
    [sg.Text('股票代码:(eg:600292)', font=("黑体", 15))],
    [sg.InputText('600292'), sg.InputCombo(concernedList, size=(20, 3))],
    [sg.Checkbox('设定该代码为常用代码', default=True)],
    [sg.Text('当前股票价格信息:', size=(20, 1), font=("黑体", 15)),
     sg.Text(nowPrice, size=(40, 1), font=("黑体", 12), key="k_nowprice")],
    [sg.Text('历史股票价格信息:', size=(30, 1), font=("黑体", 15))],
    [sg.Multiline(default_text=lastPrice, size=(40, 5), font=("黑体"), key="k_lastprice")],
    [sg.Text('_' * 80)],
    [sg.Text('新闻资讯', size=(30, 1), font=("黑体", 15))],
    [sg.Multiline(default_text=newsinfo, size=(40, 5), font=("黑体"), key="k_news")],
    [sg.Text('_' * 80)],
    [sg.Text('公司基本信息', size=(30, 1), font=("黑体", 15))],
    [sg.Multiline(default_text=baseinfo, size=(40, 5), font=("黑体"), key="k_base")],
    [sg.Text('_' * 80)],
    [sg.Text('公司财务信息', size=(30, 1), font=("黑体", 15))],
    [sg.Multiline(default_text=accountinfo, size=(40, 5), font=("黑体"), key="k_accounting")],
    [sg.Text('_' * 80)],

    [sg.OK("刷新"), sg.Cancel("取消")]
]
accountings = db.getInfos("accounting")
announcements = db.getInfos("announcement")
companys = db.getInfos("company")


def getId(code):
    for company in companys:
        if company[1] == code:
            return company[0]
    return ""


def getBaseInfo(code):
    for company in companys:
        if company[1] == code:
            return company[2], company[3], company[4]
    return "", "", ""


def getaccountingInfo(code):
    id = getId(code)
    if id != "":
        for accounting in accountings:
            if accounting[1] == id:
                return accounting[2], accounting[3]
    return "", ""


def getAnnouncements(code):
    announceList = []
    id = getId(code)
    if id != "":
        for announcement in announcements:
            if announcement[1] == id:
                announceList.append((announcement[2], announcement[3], announcement[4]))
    return announceList


def getNowPrice(code, stockprices):
    res = ""
    for i in range(len(stockprices)):
        if stockprices[len(stockprices) - i - 1][4] == code:
            price, turnover, max_price, min_price, amount, change_percentage = stockprices[len(stockprices) - i - 1][2], \
                                                                               stockprices[len(stockprices) - i - 1][3], \
                                                                               stockprices[len(stockprices) - i - 1][6], \
                                                                               stockprices[len(stockprices) - i - 1][7], \
                                                                               stockprices[len(stockprices) - i - 1][9], \
                                                                               stockprices[len(stockprices) - i - 1][10]
            res = "价格:{}|转手率:{}|涨跌幅:{}\n".format(price, turnover, change_percentage)
            break
    return res


def getLastPrice(code, stockprices):
    res = ""
    for i in range(len(stockprices)):
        if stockprices[len(stockprices) - i - 1][4] == code:
            time, price, turnover, max_price, min_price, amount, change_percentage = \
                stockprices[len(stockprices) - i - 1][1], stockprices[len(stockprices) - i - 1][2], \
                stockprices[len(stockprices) - i - 1][3], \
                stockprices[len(stockprices) - i - 1][6], \
                stockprices[len(stockprices) - i - 1][7], \
                stockprices[len(stockprices) - i - 1][9], \
                stockprices[len(stockprices) - i - 1][10]
            res += "时间:{}|价格:{}|转手率:{}|当前最高价:{}|当前最低价:{}|当前成交量:{}|涨跌幅:{}\n".format(time, price, turnover, max_price,
                                                                                   min_price,
                                                                                   amount, change_percentage)
    return res


window = mainGUI.Layout(layout)
while True:
    button, values = window.Read()
    stockprices = db.getInfos("stockprice")
    if button is not "刷新":
        break
    code = values[0]
    indus, busi, name = getBaseInfo(code)
    if indus == "":
        baseinfo = "请正确输入code值"
        indus, busi, name = getCompanyBaseInfo(code)
        baseinfo = "名称:{}\n行业:{}\n领域:{}\n".format(name, indus, busi)
    else:
        baseinfo = "名称:{}\n行业:{}\n领域:{}\n".format(name, indus, busi)
    deadtime, liabilities = getaccountingInfo(code)
    print(deadtime)
    if deadtime == "":
        accountinfo = "请正确输入code值"
        Baseurl = "http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{}/displaytype/4.phtml"
        deadtime, liabilities = parse_basic_info(Baseurl.format(code))
        liabilities = str(liabilities) + "%"
        accountinfo = "负债率:{}\n截止时间:{}\n".format(liabilities, deadtime)
    else:
        # print(liabilities)
        liabilities = str(round(liabilities, 3)) + "%"
        accountinfo = "负债率:{}\n截止时间:{}\n".format(liabilities, deadtime)
    news = getAnnouncements(code)
    if len(news) == 0:
        newsinfo = "请正确输入code值"
        names, urls, times = getCompanyAnnounceInfo(code)
        for i in range(len(names)):
            newsinfo += "事件:{}\n详细网址:{}\n报道时间:{}\n".format(names[i], urls[i], times[i])
            newsinfo += "-" * 10 + "\n"
    else:
        newsinfo = ""
        for new in news:
            name = new[2]
            url = new[1]
            time = new[0]
            newsinfo += "事件:{}\n详细网址:{}\n报道时间:{}\n".format(name, url, time)
            newsinfo += "-" * 10 + "\n"

    nowPrice = getNowPrice(code, stockprices)
    lastPrice = getLastPrice(code, stockprices)
    if nowPrice == "":
        stock_current_info_url = 'https://finance.sina.com.cn/realstock/company/{}/nc.shtml'
        stock_current_info_url = sp.create_url(code, stock_current_info_url)
        stock_current_price, stock_current_time, stock_turnover_rate, stock_flow_of_equity_rate, stock_max_price, stock_min_price, stock_opening_price, \
        stock_trading_amount, stock_change_percentage = sp.parse_stock_current_info(stock_current_info_url)
        nowPrice += "时间:{}|价格:{}|转手率:{}|当前最高价:{}|当前最低价:{}|当前成交量:{}|涨跌幅:{}\n".format(stock_current_time,
                                                                                    stock_current_price,
                                                                                    stock_turnover_rate,
                                                                                    stock_max_price, stock_min_price,
                                                                                    stock_trading_amount,
                                                                                    stock_change_percentage)
        lastPrice = nowPrice
    window.Element('k_base').Update(baseinfo)
    window.Element('k_accounting').Update(accountinfo)
    window.Element('k_news').Update(newsinfo)
    window.Element('k_nowprice').Update(nowPrice)
    window.Element('k_lastprice').Update(lastPrice)
    getImage(code)
    print(values)
