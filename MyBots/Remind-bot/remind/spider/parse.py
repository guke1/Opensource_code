# -*- coding: utf-8 -*-
"""
Created on 2021-03-02 23:40:37
---------
@summary:
---------
@author: 古客
"""

import feapder

class kktvParser(feapder.BatchParser):
    def start_requests(self, task):
        task_id = task[0]
        url = task[1]
        yield feapder.Request(url, task_id=task_id)

    def parse(self, request, response):
        title = response.xpath('//h1[@class="detail-content__title"]/span/text()')
        data = response.xpath('//script[@type="application/ld+json"]/text()')
        print(self.name, title, data)
        yield self.update_task_batch(request.task_id, 1)

class fridayParser(feapder.BatchParser):
    def start_requests(self, task):
        task_id = task[0]
        url = task[1]
        yield feapder.Request(url, task_id=task_id)

    def parse(self, request, response):
        title = response.xpath('/html/body/header/div[2]/div[1]/div/h1/text()')
        episode = response.xpath('//*[@class="episode-container"]//li/@id')
        print(self.name, title,episode)
        yield self.update_task_batch(request.task_id, 1)