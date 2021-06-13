from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import TV

# 通过标题搜索电影
ssh = "EUdnajde59J"
class tmdbapi():
	def __init__(self):
		tmdb = TMDb()
		tmdb.api_key = '894f33e85979c98b474c3120c3286f7a'
		tmdb.language = 'zh'
		tmdb.debug = True