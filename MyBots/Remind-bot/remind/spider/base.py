# -*- coding: utf-8 -*-
try:
	from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
	ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

from lxml import etree

import json
import spider.base2


class spider_data:
	def __init__(self,link):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.3683.86 Safari/537.36',
			'referer': ''
		}
		kktvlink = "https://www.kktv.me/titles/"
		fridaylink = "https://video.friday.tw/"
		if kktvlink in link:
			headers['referer'] = kktvlink
			response = spider.base2.render(link)
			response.code = 'utf-8'
			html = etree.HTML(response.text)
			ic(response.text)
			self.kktv(html)
		elif fridaylink in link:
			headers['referer'] = fridaylink
			response = spider.base2.render(link)
			response.code = 'utf-8'
			html = etree.HTML(response.text)
			ic(response.text)
			self.friday(html)

	def kktv(self, response):
		title = response.xpath('//h1[@class="detail-content__title"]/span/text()')
		data = response.xpath('//script[@type="application/ld+json"]/text()')
		ic(title,data)
		data = json.loads(data[0])
		episodes = data["containsSeason"][0]["episode"]
		for e in episodes:
			ic(e["name"])
		ic(type(episodes),episodes)

	def friday(self, response):
		title = response.xpath('/html/body/header/div[2]/div[1]/div/h1/text()')
		new = response.xpath('//*[@class="episode-container"]//li/@id')
		ic(title,new)

if __name__ == '__main__':
	link1 = "https://www.kktv.me/titles/01000190"
	link2 = "https://video.friday.tw/drama/detail/1814"
	s1 = spider_data(link1)
	s2 = spider_data(link2)