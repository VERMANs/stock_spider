# 数据库操作
import pymysql


class DB():
    def __init__(self, database):
        self.conn = pymysql.connect(
            # host="www.pomole.top",
            # user="root", password="123456",
            # database=database,
            # charset="utf8"
            host="localhost",
            user="root", password="",
            database=database,
            charset="utf8"
        )
        self.cursor = self.conn.cursor()

    # create a new table
    def createTable(self, sql):
        self.cursor.execute(sql)

    # insert some values
    def insertInfo(self, sql, values):
        self.cursor.execute(sql, values)
        self.conn.commit()

    def closeDB(self):
        # 关闭光标对象
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()

    def insertCompanyBase(self, values):
        sqlString = 'insert into company (code,industry,business,name) values (%s,%s,%s,%s);'
        self.insertInfo(sql=sqlString, values=values)

    def insertAnnouncement(self, values):
        sqlString = 'insert into announcement (companyId,date,url,name) values (%s,%s,%s,%s);'
        self.insertInfo(sql=sqlString, values=values)

    def searchCompanyBase(self, code):
        results = self.getInfos("company")
        returnString = ""
        for result in results:
            name = result[1]
            if name == code:
                returnString = result
                break
        return returnString

    def getInfos(self, tableName):
        sql = 'select * from ' + tableName + ';'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.conn.commit()
        return results


#
#
if __name__ == '__main__':
    db = DB("parse")
    infos = db.getInfos("company")
    print(infos)
    # values = ["600291", "2016-8-9", "123", "23112"]
    # db.insertAnnouncement(values)
    # print(db.searchCompanyBase("600292"))
    db.closeDB()
"""
# 定义要执行的SQL语句
sql = "CREATE TABLE USER1(\
id INT auto_increment PRIMARY KEY ,\
name CHAR(10) NOT NULL UNIQUE,\
age TINYINT NOT NULL\
)ENGINE=innodb DEFAULT CHARSET=utf8; "  # 注意：charset='utf8' 不能写成utf-8
# 执行SQL语句
cursor.execute(sql)
"""
