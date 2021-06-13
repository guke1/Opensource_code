from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from telebot import types
import douban
import tmdbapi
import userfile
import logging

tmdb = tmdbapi.tmdbapi()
TOKEN = '1566719375:AAGuyUnHIWbAns3zCUvL917GEbqOa82d4qg'
telebot.logger.setLevel(logging.DEBUG)
douBan = douban.DoubanSpider()
f = userfile.userfile()
knownUsers = []  # todo: save these in a file,
userStep = {}  # 这样他们就不会在每次机器人重启的时候重置
commands = {  # 帮助 "命令中使用的命令描述
	'start': '欢迎使用古客的影片信息查询机器人',
	'help': '获取帮助',
	'tmdb': 'tmdb信息查询',
	'douban': '豆瓣信息查询'
}

modeSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
modeSelect.add('电影', '剧集')

hideBoard = types.ReplyKeyboardRemove()  # 如果以response_markup方式发送，将隐藏键盘


# 如果用户不知道，错误处理
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
	if uid in userStep:
		return userStep[uid]
	else:
		knownUsers.append(uid)
		userStep[uid] = 0
		print("检测到新用户，他没有使用过 \"/start\"")
		return 0


# 内联键盘
def gen_markup(movies=[""]):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	for name in movies:
		markup.add(InlineKeyboardButton(name, callback_data=("douban"+name)))
	return markup


def gen_markup2(movies=[""]):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	for index,name in enumerate(movies):
		markup.add(InlineKeyboardButton(name, callback_data=("tmdb" + str(index))))
	return markup

bot = telebot.TeleBot(TOKEN)


@bot.callback_query_handler(func=lambda call: call.data[0:6] == "douban")
def callback_query(call):
	m = douBan.moviedict()
	call.data = call.data.replace("douban","")
	link = m[call.data]
	movieData = douBan.get_data(link)
	pic = movieData[0]
	data = movieData[1]
	over = movieData[2]
	print(call)
	bot.answer_callback_query(call.id, "正在查询，请稍等片刻...")
	i = 0
	@bot.message_handler(func=lambda message: True)
	def data_step(m):
		i = 0
		if i == 0:
			cid = m.chat.id
			bot.send_photo(cid, pic[0], reply_markup=hideBoard)
			bot.send_message(cid, data)
			bot.send_message(cid, over)
			i = 1
	data_step


@bot.callback_query_handler(func=lambda call: call.data[0:6] == "tmdb")
def callback_query(call):
	call.data = call.data.replace("tmdb", "")
	print(call)
	bot.answer_callback_query(call.id, "正在查询，请稍等片刻...")
	data = tmdb.TVName()
	i = 0
	@bot.message_handler(func=lambda message: True)
	def data_step(m):
		i = 0

		if i == 0:
			cid = m.chat.id
			bot.send_photo(cid, pic[0], reply_markup=hideBoard)
			bot.send_message(cid, data)
			i = 1
	data_step
# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
	cid = m.chat.id
	if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
		knownUsers.append(cid)  # 保存用户ID，这样你就可以在以后向这个机器人的所有用户广播消息了
		userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
		bot.send_message(cid, "欢迎使用古客的影片信息查询机器人")
		command_help(m)  # 向新用户展示帮助页面
	else:
		bot.send_message(cid, "欢迎再次使用")


# 帮助页面
@bot.message_handler(commands=['help'])
def command_help(m):
	cid = m.chat.id
	help_text = "以下是可用的命令: \n"
	for key in commands:  # generate help text out of the commands dictionary defined at the top
		help_text += "/" + key + ": "
		help_text += commands[key] + "\n"
	bot.send_message(cid, help_text)  # 发送生成的帮助页面

# 豆瓣信息查询
@bot.message_handler(commands=['douban'])
def command_douban(m):
	cid = m.chat.id
	msg = bot.send_message(cid, "请输入需要查询的影片名")
	bot.register_next_step_handler(msg,name_step)


def name_step(m):
	try:
		cid = m.chat.id
		text = m.text
		if len(text) > 0:
			douBan.main(text)
			print(text)
			movies = douBan.movielist()
			bot.send_message(cid, "查询结果如下，请选择其中一个:", reply_markup=gen_markup(movies))
	except Exception as e:
		bot.reply_to(m,'似乎出问题了')


# tmdb信息查询
@bot.message_handler(commands=['tmdb'])
def command_tmdb(m):
	cid = m.chat.id
	bot.send_message(cid, "请选择影片类型", reply_markup=modeSelect)  # show the keyboard
	userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)


# if the user has issued the "/tmdb" command, process the answer
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
	cid = m.chat.id
	text = m.text
	bot.send_chat_action(cid, 'typing')

	if text == '电影':
		msg = bot.send_message(cid, "请输入需要查询的影片名")
		bot.register_next_step_handler(msg, name_step2)
		bot.send_photo(cid, 'https://cdn.jsdelivr.net/gh/guhailong18/blog/medias/featureimages/7.jpg',reply_markup=hideBoard)  # 发送文件和隐藏键盘，在图像发送后
		userStep[cid] = 0  # reset the users step back to 0
	elif text == '剧集':
		msg = bot.send_message(cid, "请输入需要查询的影片名")
		bot.register_next_step_handler(msg, name_step3)
		bot.send_photo(cid, 'https://cdn.jsdelivr.net/gh/guhailong18/blog/medias/featureimages/18.jpg',reply_markup=hideBoard)
		userStep[cid] = 0
	else:
		bot.send_message(cid, "Please, use the predefined keyboard!")
		bot.send_message(cid, "请重试")


def name_step2(m):
	try:
		cid = m.chat.id
		text = m.text
		if len(text) > 0:
			ll = tmdb.MovieName(text)
			movies = []
			for l in ll:
				movies.append(l['title'])
			bot.send_message(cid, "查询结果如下，请选择其中一个:", reply_markup=gen_markup(movies))
	except Exception as e:
		bot.reply_to(m, '似乎出问题了')


def name_step3(m):
	try:
		cid = m.chat.id
		text = m.text
		if len(text) > 0:
			ll = tmdb.TVName(text)
			movies = []
			for l in ll:
				movies.append(l['name'])
			bot.send_message(cid, "查询结果如下，请选择其中一个:", reply_markup=gen_markup(movies))
	except Exception as e:
		bot.reply_to(m, '似乎出问题了')

# 筛选特定信息
@bot.message_handler(func=lambda message: message.text == "古客")
def command_text_hi(m):
	bot.send_message(m.chat.id, "你是最帅的!")

bot.polling()