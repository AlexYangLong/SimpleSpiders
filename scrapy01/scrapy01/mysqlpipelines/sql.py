from .mySqlDBTools import MySqlDBTools
from scrapy01.scrapy01 import settings


mysql = MySqlDBTools(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.MYSQL_DB, settings.MYSQL_PORT)

