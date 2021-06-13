import logging
from typing import Dict
import os
import shutil
from time import sleep
from sub import subs
import zipfile
import rarfile
from telegram import ReplyKeyboardMarkup, Update, File, TelegramError, Voice
from telegram.ext import (
	Updater,
	CommandHandler,
	MessageHandler,
	Filters,
	ConversationHandler,
	CallbackContext,
)

# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
	['简转繁', '繁转简'],
	['简转台湾', '台湾转简'],
	['繁转日文', '日文转繁'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
	facts = list()

	for key, value in user_data.items():
		facts.append(f'{key} - {value}')

	return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Hi!这是字幕转换机器人,"
		"使用 /sub 选择模式,再发送字幕文件,并进行转换"
	)
	user = update.message.from_user
	logger.info("User %s started the conversation.", user.first_name)
	return CHOOSING


def sub(update: Update, context: CallbackContext) -> int:
	update.message.reply_text(
		"请选择转换模式",
		reply_markup=markup,
	)
	return CHOOSING

def get_sub(update: Update, context: CallbackContext):
	text = update.message.text
	chat_id = update.message.chat_id
	context.user_data['choice'] = text
	update.message.reply_text(f'你选择的转换模式是{text}，请发送字幕文件(仅支持.ass/.srt)或压缩文件(仅支持.zip/.rar)')
	user = update.message.from_user
	logger.info("User %s 选择的模式是: %s", user.first_name, text)



def un_zip(sub_file,c):
	zFile = zipfile.ZipFile(sub_file, "r")
	_sub_file = sub_file[:-4]
	if os.path.isdir(_sub_file):
		pass
	else:
		os.mkdir(_sub_file)
	zFile.extractall(_sub_file)
	zFile.close()
	for root, dirs, files in os.walk('./'+_sub_file):
		for f in files:
			f = './' + _sub_file + '/' + f
			subs(f,c)
	os.remove(sub_file)
	make_zip(_sub_file,sub_file)


def make_zip(source_dir, output_filename):
	zipf = zipfile.ZipFile(output_filename, 'w')
	pre_len = len(os.path.dirname(source_dir))
	for parent, dirnames, filenames in os.walk(source_dir):
		for filename in filenames:
			pathfile = os.path.join(parent, filename)
			arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
			zipf.write(pathfile, arcname)
	zipf.close()
	shutil.rmtree(source_dir)

def un_rar(sub_file,c):
	rar = rarfile.RarFile(sub_file, "r")
	_sub_file = sub_file[:-4]
	if os.path.isdir(_sub_file):
		pass
	else:
		os.mkdir(_sub_file)
	rar.extractall(_sub_file)
	rar.close()
	for root, dirs, files in os.walk('./'+_sub_file):
		print(files)
		for f in files:
			f = './'+_sub_file+'/'+f
			print(f)
			subs(f, c)
	os.remove(sub_file)
	make_zip(_sub_file,sub_file)

def sub_rename(old, new):
	os.rename(old, new)
	return new


def done(update: Update, context: CallbackContext) -> int:
	chat_id = update.message.chat_id
	user_data = context.user_data
	text = user_data['choice']
	sub_file = context.bot.get_file(update.message.document).download()
	sub_file_ = sub_file[-4:]
	if sub_file_ == '.zip':
		s = "识别为zip文件，正在进行解压"
		un_zip(sub_file,text)
		update.message.reply_text(s)
		sleep(8)
		if os.path.exists(sub_file):
			context.bot.sendDocument(chat_id=chat_id, document=open(sub_file, 'rb'))
			os.remove(sub_file)
	elif sub_file_ == ".rar":
		s = "识别为rar文件，正在进行解压"
		un_rar(sub_file,text)
		update.message.reply_text(s)
		sleep(8)
		if os.path.exists(sub_file):
			context.bot.sendDocument(chat_id=chat_id, document=open(sub_file, 'rb'))
			os.remove(sub_file)
	elif sub_file_ in ['.ass', '.srt', '.ssa', '.smi']:
		s = "识别为单字幕文件"
		update.message.reply_text(s)
		if subs(sub_file, str(text)):
			context.bot.sendDocument(chat_id=chat_id, document=open(sub_file, 'rb'))
			os.remove(sub_file)
	else:
		s = "该文件格式无法识别"
		update.message.reply_text(s)
	update.message.reply_text(
		f"转换完成,欢迎下次使用！"
	)
	if 'choice' in user_data:
		del user_data['choice']
	user_data.clear()
	return ConversationHandler.END

def main() -> None:
	# Create the Updater and pass it your bot's token.
	updater = Updater("1622260408:AAFQhouKSLfIxjtanDLtI2qFVUhlwXlOUyE", use_context=True)

	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher

	# Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('sub', sub)],
		states={
			CHOOSING: [
				MessageHandler(
					Filters.regex('^(简转繁|繁转简|简转台湾|台湾转简|繁转日文|日文转繁)$'), get_sub
				)
			],
		},
		fallbacks=[MessageHandler(Filters.document & ~(Filters.text | Filters.command | Filters.regex('^Done$')), done)],
	)

	dispatcher.add_handler(conv_handler)
	dispatcher.add_handler(CommandHandler("start", start))
	updater.dispatcher.add_handler(MessageHandler(Filters.document, get_sub))

	# Start the Bot
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()