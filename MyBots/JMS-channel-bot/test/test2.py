import spider

link = "https://movie.douban.com/subject/2129283"
link2 = "https://www.themoviedb.org/tv/96737"
link3 = "https://www.themoviedb.org/tv/34667-maria-holic"
s = spider.spider(link)
data = ["", ""]
data[0] = s.data[3]
data[1] = s.str_data
print(data)