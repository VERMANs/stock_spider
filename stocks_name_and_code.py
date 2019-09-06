import requests
from lxml import etree

def parse_stocks_name_and_code():
    url = 'http://quote.eastmoney.com/stock_list.html'
    headers = {
               'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        }
    r = requests.get(url=url, headers=headers)
    r.encoding = 'gbk'
    tree = etree.HTML(r.text)
    list = tree.xpath('//div[@id="quotesearch"]//li/a/text()')
    #fp2 = open('./stocks.txt', 'w', encoding='utf8')
    names = []
    codes = []
    for item in list:
        name = item.split('(')[0]
        number = item.split('(')[-1].strip(')')
        names.append(name)
        codes.append(number)
        #fp2.write(name)
        #fp2.write(number)
        #fp2.write('\n')
    #fp2.close()
    return names, codes

def search_a_company(key_word, names, codes):
    if(str(key_word).isdigit()):
        for i in range(len(codes)):
            if(codes[i] == key_word):
                return names[i]
    else:
        for i in range(len(names)):
            if(names[i] == key_word):
                return codes[i]

def parse_and_convert(key_word):
    # 此处可以优化：第一次运行时可以去parse，parse过程把文件下载下来，之后加一个文件存在的判断，如果文件存在就可以直接访问文件，不需要重复爬取
    names, codes = parse_stocks_name_and_code()
    company = search_a_company(key_word, names, codes)
    return company

#
# if __name__ == "__main__":
#     names, codes = parse_stocks_name_and_code()
#     key_word = input("请输入你要查找的公司名称或代码:")
#     company = search_a_company(key_word, names, codes)
#     print(company)