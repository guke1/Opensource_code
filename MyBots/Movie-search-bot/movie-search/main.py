# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import douban
spider = douban.DoubanSpider()
spider.main("超人")
print(spider.get_data("https://movie.douban.com/subject/10512661/"))