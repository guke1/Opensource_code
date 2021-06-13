import requests
from lxml import etree
from fake_useragent import UserAgent
import time
import random


class DoubanSpider(object):
    def __init__(self):
        self.url = 'https://www.douban.com/search?q={}'
        self.dd_list = [""]
        ua = UserAgent(verify_ssl=False)
        for i in range(1, 50):
            self.headers = {
                'User-Agent': ua.random,
            }

    # 获取页面
    def get_page(self, url):
        # random.choice一定要写在这里,每次请求都会随机选择
        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        self.parse_page(html)

    # 解析页面
    def parse_page(self, html):
        # 　创建解析对象
        parse_html = etree.HTML(html)
        # 基准xpath节点对象列表
        dd_list = parse_html.xpath('//div[@class="result-list"]//h3')
        self.dd_list = dd_list

    def movielist(self):
        dd_list = self.dd_list
        movielist = []
        for dd in dd_list[:10]:
            name = dd.xpath('.//a/text()')[0].strip()
            movielist.append(name)
        return movielist

    def moviedict(self):
        dd_list = self.dd_list
        moviedct = {}
        for dd in dd_list[:10]:
            link = dd.xpath('.//a/@href')[0].strip()
            name = dd.xpath('.//a/text()')[0].strip()
            moviedct[name]=link
        return moviedct


    # 主函数
    def main(self, name=""):
        url = self.url.format(str(name))
        self.get_page(url)
        time.sleep(random.randint(1, 3))

    def get_data(self, link):
        res = requests.get(link, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        parse_html = etree.HTML(html)
        dd = parse_html
        data = dd.xpath('//div[@id="info"]//text()')
        data1 = []
        for d in data:
            data1.append(d.strip())
        data = "".join(data1)
        pic = dd.xpath('//*[@id="mainpic"]/a/img/@src')
        content = dd.xpath('//*[@id="link-report"]/span[@property="v:summary"]//text()')
        content1 = []
        for c in content:
            content1.append(c.strip())
        content = "".join(content1)
        l = [pic,data,content]
        return l

if __name__ == '__main__':
    spider = DoubanSpider()
    spider.main("超人")