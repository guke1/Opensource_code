from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import TV

# 通过标题搜索电影

class tmdbapi():
	def __init__(self):
		tmdb = TMDb()
		tmdb.api_key = '894f33e85979c98b474c3120c3286f7a'
		tmdb.language = 'zh'
		tmdb.debug = True


	def MovieName(name):
		movie = Movie()
		movie.language = 'zh'
		search = movie.search(name)
		return search

	def get_title(self):

	# 通过标题搜索电视剧

	def TVName(name):
		tv = TV()
		tv.language = 'zh'
		search = tv.search(name)
		return search

	def get_data(self):