# -*- coding: utf-8 -*-
# 作者：古客
# 日期：2021/6/13 19:11
# 工具：PyCharm
import remind_bot, spider_main, db, spider

# 初始化数据库
sql_db = db.sql.db()
sql_db.create_table()
# 启动爬虫
spider_main.batch_spider_integration_test(1)
spider_main.batch_spider_integration_test(2)
# 启动bot
remind_bot.main()