# -*- coding: utf-8 -*-
import requests, json
from urllib.parse import quote


def render(link):
	kktvlink = "https://www.kktv.me/titles/"
	fridaylink = "https://video.friday.tw/"
	css = ""
	script = """
	splash.images_enabled = false
	assert(splash:go(args.url))
	assert(splash:wait(0.5))
	s = splash:select(args.css)
	s:mouse_click()
	splash:wait(0.3)
	return splash:html()
	"""

	if kktvlink in link:
		css = """#__next > div.layout > main > div > div.video-detail__panel > div.video-detail__content > div.tabs > ul > li:nth-child(2) > a > span"""
	elif fridaylink in link:
		css = """body > header > div.header-content > div.header-text > div > h1"""
	response = requests.post('http://107.173.165.137:8050/run', json={
		'lua_source': script,
		'url': link,
		'css': css,
	})
	return response

if __name__ == '__main__':
	kktc = render("https://www.kktv.me/titles/01000190")
	friday = render("https://video.friday.tw/drama/detail/1814")
	print(kktc.text, friday.text)