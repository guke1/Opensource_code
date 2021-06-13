# -*- coding: utf-8 -*-
from feapder import Item


class SpiderDataItem(Item):
	def __init__(self, *args, **kwargs):
		# self.id = None  # type : int(10) unsigned | allow_null : NO | key : PRI | default_value : None | extra : auto_increment | column_comment :
		self.title = None  # type : varchar(255) | allow_null : YES | key :  | default_value : None | extra : | column_comment :


def test(**kwargs):
	for key, value in kwargs.items():
		key = value
	print(key)


test(s="1")