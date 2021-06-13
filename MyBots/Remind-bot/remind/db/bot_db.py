# -*- coding: utf-8 -*-
import time
import db.sql


class botdb(db.sql.db):
	def __init__(self):
		db.sql.db.__init__(self)

	def add_user(self, user_id,user_name):
		"""添加用户"""
		mysqldb = self.mysqldb
		table_name = "bot_users"
		start_time = self.get_time()
		data = {"user_id":user_id,"user_name":user_name, "start_time":start_time}
		if mysqldb.add_smart(table_name, data):
			return True
		else:
			return False

	def update_user(self,user_id,user_name):
		"""更新用户信息"""
		mysqldb = self.mysqldb
		table_name = ""
		

	def del_user(self,user_id):
		"""删除用户"""
		mysqldb = self.mysqldb
		table_name = ""
		self.delete_db(table_name)

	def add_link(self,link,user_id=""):
		"""添加链接"""
		mysqldb = self.mysqldb
		table_name = "bot_links"
		data = {"link":link,"user_id":user_id}
		if not self.has_link(table_name,link):
			mysqldb.add_smart(table_name,data)
		table_name = "batch_spider_integration_task"
		if self.has_link(table_name,link):
			data = {"link": link,"subscribe_number": 2}
			mysqldb.add_smart(table_name,data)
		else:
			data = {"link": link}
			mysqldb.add_smart(table_name,data)

	def del_link(self,link):
		"""删除链接"""
		mysqldb = self.mysqldb
		table_name = ""
		mysqldb.delete()
		self.delete_db(table_name)
		
	def get_links(self,user_id):
		"""获取用户所有链接"""
		mysqldb = self.mysqldb
		select_sql = f"select * from bot_links where user_id = {user_id}"
		data = mysqldb.find(select_sql)
		return data
		
	def create_group(self,group_name,user_id):
		"""创建组"""
		mysqldb = self.mysqldb
		table_name = "group"
		group_id = hash(group_name + self.get_time())
		data = {"group_id": group_id,"user_id":user_id,"group_name":group_name,"is_admin":1}
		mysqldb.add_smart(table_name,data)

	def del_group(self,group_name):
		"""删除组"""
		mysqldb = self.mysqldb
		table_name = ""
		self.delete_db(table_name)



	@staticmethod
	def get_time():
		now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		return now

if __name__ == "__main__":
	db = botdb()
	db.create_table()
	print(db.get_time())