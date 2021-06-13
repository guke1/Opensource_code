# -*- coding: utf-8 -*-
import os
from feapder.db.mysqldb import MysqlDB
from feapder.utils.tools import list2str, format_sql_value


def read_sql(sqlfile):
    sql_text = []
    if os.path.isfile(sqlfile):
        with open(sqlfile, "r", encoding='utf-8') as f:
            sql = f.readlines()
            for s in sql:
                if "#" in s[:2] or "--" in s[:2]:
                    pass
                elif "/*" in s[:2] or "*/" in s[:-2]:
                    pass
                else:
                    s = s.strip('\n').strip()
                    sql_text.append(s)
    sql = "".join(sql_text)
    sqlCommands = sql.split(';')
    return sqlCommands


def make_delete_sql(table, data):
    keys = ["`{}`".format(key) for key in data.keys()]
    keys = list2str(keys).replace("'", "")
    values = [format_sql_value(value) for value in data.values()]
    values = list2str(values)
    sql = f"DELETE FROM {table} WHERE {keys}={values}"
    sql = sql.replace("None", "null")
    return sql


def make_select_sql(table, data):
    keys = ["`{}`".format(key) for key in data.keys()]
    keys = list2str(keys).replace("'", "")

    values = [format_sql_value(value) for value in data.values()]
    values = list2str(values)
    sql = f"SELECT * FROM {table} WHERE {keys}={values}"
    sql = sql.replace("None", "null")
    return sql


class db:
    def __init__(self):
        self.mysqldb = MysqlDB(
            ip="193.123.253.216", port=3306, db="feapder", user_name="feapder", user_pass="feapder"
        )

    def get_mysql_imformation(self):
        """获取数据库信息"""
        mysqldb = self.mysqldb
        databases = [x[0] for x in mysqldb.find("SHOW DATABASES")]  # [("",)]
        user_database = mysqldb.find("select database()")[0][0]
        tables = [x[0] for x in mysqldb.find("SHOW TABLES")]
        version_info = mysqldb.find("SELECT VERSION()")[0][0]
        pool_connections = mysqldb.size_of_connect_pool()
        acti_connections = mysqldb.size_of_connections()
        data = f"""
所有数据库: {databases};
当前使用的数据库: {user_database};所有表: {tables};
数据库版本: {version_info};
总连接数: {pool_connections}; 活跃连接数: {acti_connections}"""
        return data

    def get_table_details(self, tablename, database=""):
        """获取表信息"""
        mysqldb = self.mysqldb
        if database:
            mysqldb.execute(f"use {database}")
        a = mysqldb.find(f"DESC {tablename}")[0]
        b = mysqldb.find(f"SHOW CREATE TABLE {tablename}")[0]
        c = mysqldb.find(f"SHOW TABLE STATUS LIKE '{tablename}'")[0]
        table_detail = f"""
字段: {a};
建表语句: {b};
详细信息: {c}"""
        return table_detail

    def create_table(self):
        mysqldb = self.mysqldb
        sqlcommand = read_sql("table.sql")
        for s in sqlcommand:
            if s:
                mysqldb.execute(s)
        return None

    def drop_table(self, tablename):
        mysqldb = self.mysqldb
        drop_sql = f"DROP TABLE {tablename}"
        mysqldb.delete(drop_sql)
        return None

    def copy_table(self, tablename):
        mysqldb = self.mysqldb
        create_sql = rf"SHOW CREATE TABLE {tablename} \G"
        create_sql = mysqldb.find(create_sql)

    def delete_db(self, table_name, data):
        """删除数据"""
        mysqldb = self.mysqldb
        delete_sql = make_delete_sql(table_name,data)
        data = mysqldb.delete(delete_sql)
        return data

    def search_db(self, table_name,data):
        """查询数据"""
        
        select_sql = make_select_sql(table_name,data)

    def get_link_information(self):
        """获取链接信息"""
        mysqldb = self.mysqldb
        select_sql = ""
        data = mysqldb.find(select_sql)
        return data

    def get_user_information(self):
        """admin:使用者信息"""
        mysqldb = self.mysqldb
        select_sql = make_select_sql("")
        data = mysqldb.find(select_sql)
        return data

    def get_group_information(self):
        """获取组信息"""
        mysqldb = self.mysqldb
        select_sql = ""
        data = mysqldb.find(select_sql)
        return data

    def has_link(self, table_name, link):
        """链接是否存在"""
        mysqldb = self.mysqldb
        select_sql = f"SELECT * from {table_name} WHERE link='{link}' limit 1"
        data = mysqldb.find(select_sql)
        if data:
            return True
        else:
            return False

    def has_user(self, table_name, user_id):
        """用户是否存在"""
        mysqldb = self.mysqldb
        select_sql = f"SELECT * from {table_name} WHERE user_id = '{user_id}'"
        data = mysqldb.find(select_sql)
        if data:
            return True
        else:
            return False


if __name__ == "__main__":
    d = db()
    d.create_table()