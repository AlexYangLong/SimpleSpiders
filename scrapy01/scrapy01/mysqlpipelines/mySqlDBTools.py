import pymysql
from scrapy01 import settings


HOST = settings.MYSQL_HOST
USER = settings.MYSQL_USER
PASSWORD = settings.MYSQL_PASSWORD
PORT = settings.MYSQL_PORT
DB = settings.MYSQL_DB


class MySqlDBTools(object):
    def __init__(self):
        self.ip = HOST
        self.username = USER
        self.password = PASSWORD
        self.dbName = DB
        self.port = PORT

    # 连接数据库服务
    def connectDB(self):
        self.conn = pymysql.connect(self.ip, self.username, self.password, self.dbName, port=int(self.port), charset='utf8')
        # print(self.conn)
        self.cursor = self.conn.cursor()
        #return self.cursor

    # 关闭数据库连接
    def closeDB(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    #执行查询语句，并返回查询出的结果，一个元组
    def dqlExecute(self, sql):
        res = ()
        try:
            self.connectDB()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
        except BaseException as e:
            print("查询出错！", e)
        finally:
            self.closeDB()

        return res

    #执行insert、update、delete语句，并返回影响的行数
    def dmlExecute(self, sql):
        count = 0
        try:
            self.connectDB()
            count = self.cursor.execute(sql)
            self.conn.commit()
        except BaseException as e:
            print("事物提交失败！", e)
            self.conn.rollback()
        finally:
            self.closeDB()

        return count








