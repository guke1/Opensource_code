from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from telebot import types
import logging
import spider
import time

TOKEN = '1583947472:AAF4R2rHkTlUQ_8hg0TixFh8kuMOGt08t7M'
logger = telebot.logger
# telebot.logger.basicConfig(filename='jms-bot.log', level=logging.DEBUG,format=' %(asctime)s - %(levelname)s - %(
# message)s')
telebot.logger.setLevel(logging.DEBUG)
knownUsers = []  # todo: save these in a file,
userStep = {}  # 这样他们就不会在每次机器人重启的时候重置
commands = {  # 帮助 "命令中使用的命令描述
	'start': '欢迎使用JMS频道机器人'
}
markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
itembtna = types.KeyboardButton('是')
itembtnv = types.KeyboardButton('是,无介绍')
itembtnc = types.KeyboardButton('否')
itembtnd = types.KeyboardButton('否,直接发送')
markup.row(itembtna, itembtnv)
markup.row(itembtnc, itembtnd)

markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True)
markup1.add('是', '否')

modeSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
hideBoard = types.ReplyKeyboardRemove()  # 如果以response_markup方式发送，将隐藏键盘。
new_data = ["", "", ""]


def get_user_step(uid):
	if uid in userStep:
		return userStep[uid]
	else:
		knownUsers.append(uid)
		userStep[uid] = 0
		print("检测到新用户，他没有使用过 \"/start\"")
		return 0


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_start(m):
	cid = m.chat.id
	if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
		knownUsers.append(cid)  # 保存用户ID，这样你就可以在以后向这个机器人的所有用户广播消息了
		userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
		bot.send_message(cid, "欢迎使用JMS频道机器人")
	else:
		bot.send_message(cid, "欢迎再次使用")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
	global new_data
	link = message.text
	cid = message.chat.id
	try:
		if "http" in link:
			s = spider.spider(link)
			new_data[0] = s.data[3]
			new_data[1] = s.str_data
			new_data[2] = s.str_data1
			bot.send_photo(cid, s.data[3], s.str_data, parse_mode="Markdown")
			msg = bot.send_message(cid, "是否需要修改消息", reply_markup=markup)
			bot.register_next_step_handler(msg, edit_step)
		else:
			bot.send_message(cid, "请发送豆瓣/TMDB的链接")
	except Exception as e:
		print(e)
		bot.send_message(cid, f"似乎出了点小问题,请检查链接是否正确,代码报错{e}")


def edit_step(m):
	cid = m.chat.id
	text = m.text
	try:
		if text == "是":
			msg = bot.send_message(cid, "请发送需要添加的信息")
			bot.register_next_step_handler(msg, data_step)
		elif text == "是,无介绍":
			msg = bot.send_message(cid, "请发送需要添加的信息")
			bot.register_next_step_handler(msg, data_step2)
		elif text == "否":
			msg = bot.send_message(cid, "是否直接发送到群组", reply_markup=markup1)
			bot.register_next_step_handler(msg, send_step)
		elif text == "否,直接发送":
			group_id = "-1001322576129"  # -1001322576129 JMS -1001482303269 测试
			bot.send_photo(group_id, new_data[0], new_data[2], parse_mode="Markdown")
	except Exception as e:
		print(e)
		bot.send_message(cid, "修改失败，请联系@guke18")


def data_step(m):
	global new_data
	cid = m.chat.id
	text = m.text
	data = new_data[1].split("\n", 3)
	data[2] = data[2] + "\n" + text
	new_data[1] = "\n".join(data)
	bot.send_photo(cid, new_data[0], new_data[1], parse_mode="Markdown")
	msg = bot.send_message(cid, "修改成功,结果如上，是否直接发送到群组", reply_markup=markup1)
	try:
		bot.register_next_step_handler(msg, send_step)
	except Exception as e:
		print(e)
		bot.send_message(cid, "似乎出了点问题", e)


def data_step2(m):
	global new_data
	cid = m.chat.id
	text = m.text
	data = new_data[2].split("\n", 3)
	print("data:", data)
	data[-1] = text + "\n" + data[-1]
	new_data[2] = "\n".join(data)
	bot.send_photo(cid, new_data[0], new_data[2], parse_mode="Markdown")
	msg = bot.send_message(cid, "修改成功,结果如上，是否直接发送到群组", reply_markup=markup1)
	try:
		bot.register_next_step_handler(msg, send_step2)
	except Exception as e:
		print(e)
		bot.send_message(cid, "似乎出了点问题", e)


def send_step(m):
	group_id = "-1001322576129"  # -1001322576129 JMS -1001482303269 测试
	text = m.text
	if text == "是":
		bot.send_photo(group_id, new_data[0], new_data[1], parse_mode="Markdown")


def send_step2(m):
	group_id = "-1001322576129"  # -1001322576129 JMS -1001482303269 测试
	text = m.text
	if text == "是":
		bot.send_photo(group_id, new_data[0], new_data[2], parse_mode="Markdown")


# 筛选特定信息
@bot.message_handler(func=lambda message: message.text == "古客")
def command_text_hi(m):
	bot.send_message(m.chat.id, "你是最帅的!")


while True:
	try:
		bot.polling(none_stop=True)
	# ConnectionError和ReadTimeout，因为请求库可能超时
	# TypeError for moviepy错误
	except Exception as e:
		time.sleep(15)