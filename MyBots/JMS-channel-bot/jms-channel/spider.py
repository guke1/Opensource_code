import requests
from lxml import etree
from fake_useragent import UserAgent
import time
import random
import re
from feapder import Request

class spider(object):
	def __init__(self, link):
		self.url = link
		ua = UserAgent(verify_ssl=False)
		for i in range(1, 50):
			self.headers = {
				'User-Agent': ua.random,
			}
		# random.choice一定要写在这里,每次请求都会随机选择
		res = requests.get(link, headers=self.headers)
		res.encoding = 'utf-8'
		html = res.text
		# 　创建解析对象
		parse_html = etree.HTML(html)
		if "douban" in link:
			self.douban(parse_html)
		elif "themoviedb.org" in link:
			link = link + "?language=zh-CN"
			res = requests.get(link, headers=self.headers)
			res.encoding = 'utf-8'
			html = res.text
			parse_html = etree.HTML(html)
			self.tmdb(parse_html)

	def douban(self, html):
		data = []
		link = self.url
		title = html.xpath('//*[@id="content"]/h1/span[@property="v:itemreviewed"]/text()')[0]
		t1 = title.split()[0]
		try:
			t2 = title.split()[1]
		except IndexError:
			t2 = ""
		year = html.xpath('//*[@id="content"]/h1/span[2]/text()')[0]
		over = html.xpath('//div[@id="link-report"]//span[@property="v:summary"]//text()')[0]
		pic = html.xpath('//*[@id="mainpic"]/a/img/@src')[0]
		try:
			score = "豆瓣" + html.xpath('//*[@id="interest_sectl"]//strong[@property="v:average"]/text()')[0]
		except Exception as e:
			score = "暂无评分"
			print(e)
		d = "⚡ emby使用方法 (https://t.me/CurlyMouse/199)"
		over = str_replace(over)
		title = str_replace(title)
		data.append(title)
		data.append(year)
		data.append(over)
		data.append(pic)
		data.append(d)
		str_data = """%s %s
[%s](%s)
#%s

介绍:
%s

⚡[卷毛鼠公益服EMBY使用方法](https://t.me/CurlyMouse/199)""" % (title, year, score, link, t1, over.strip())
		str_data1 = """%s %s
[平均评分:%s](%s)
#%s

⚡[卷毛鼠公益服EMBY使用方法](https://t.me/CurlyMouse/199)""" % (title, year, score, link, title)
		self.str_data = str_data
		self.data = data
		self.str_data1 = str_data1


	def tmdb(self, html):
		data = []
		# title = html.xpath('//div[@class="title ott_false"]/h2/a/text()')[0]
		link = self.url
		title = html.xpath('//*[@id="original_header"]//div[starts-with(@class,"title")]/h2/a/text()')[0]
		year = html.xpath('//*[@id="original_header"]//span[@class="tag release_date"]/text()')[0]
		over = html.xpath('//div[@class="overview"]//p//text()')[0]
		pic = "https://www.themoviedb.org/" + html.xpath('//img[@class="poster lazyload"]/@data-srcset')[0]
		pic = re.match(r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', pic).group(0)
		try:
			score = html.xpath('//*[@id="original_header"]//div[@class="user_score_chart"]/@data-percent')[0]
		except Exception as e:
			score = "暂无分数"
		over = str_replace(over)
		title = str_replace(title)
		data.append(title)
		data.append(year)
		data.append(over)
		data.append(pic)

		str_data = """%s %s
[平均评分:%s](%s)
#%s

介绍:
%s

⚡[卷毛鼠公益服EMBY使用方法](https://t.me/CurlyMouse/199)""" % (title, year, score, link, title, over.strip())
		str_data1 = """%s %s
[平均评分:%s](%s)
#%s

⚡[卷毛鼠公益服EMBY使用方法](https://t.me/CurlyMouse/199)""" % (title, year, score, link, title)
		self.str_data = str_data
		self.data = data
		self.str_data1 = str_data1

def str_replace(s1):
	if "*" or "_" in s1:
		s1 = s1.replace("_", " ", 2)
		s1 = s1.replace("*", " ", 2)
	return s1