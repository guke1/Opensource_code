import logging, json, html, traceback
from typing import Tuple, Optional, Dict, Set
import db.bot_db
from telegram import Update, Chat, ChatMember, ParseMode, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    ChatMemberHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    TypeHandler,
    Dispatcher,
)


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)
botdb = db.bot_db.botdb()
support_website = ["www.kktv.me", "video.friday.tw"]

# 这可以是您自己的 ID，也可以是开发者群组频道的 ID。
DEVELOPER_CHAT_ID = 1050885726

def start(update: Update, context: CallbackContext):
    chat = update.effective_chat
    logger.info(f"""chat: {chat}""")
    text = "欢迎使用提醒机器人，使用/help查看帮助信息"
    context.bot.send_message(chat_id=chat.id, text=text)


def register(update: Update, context: CallbackContext):
    """注册"""
    chat = update.effective_chat
    if botdb.add_user(chat.id, chat.username):
        text = "注册成功"
    else:
        text = "出现未知异常，注册失败"
    context.bot.send_message(chat_id=chat.id, text=text)

# 链接
def list_link(update: Update, context: CallbackContext):
    """发送订阅链接列表"""
    chat = update.effective_chat
    try:
        link_list = botdb.get_links(chat.id)
        text = "\n".join(link_list)
    except Exception as e:
        text = "获取数据异常"
    context.bot.send_message(chat_id=chat.id, text=text)

def add_link(update: Update, context: CallbackContext):
    """添加链接"""
    chat = update.effective_chat

def remove_link(update: Update, context: CallbackContext):
    """删除链接"""
    chat = update.effective_chat

def check_link(update: Update, context: CallbackContext):
    """自动检测链接"""
    chat = update.effective_chat
    link = update.message.text
    if "http" in link:
        text = "检测到为链接,正在尝试订阅"
        context.bot.send_message(chat_id=chat.id, text=text)
        for s in support_website:
            if s in link:
                botdb.add_link(link,chat.id)
                text = "该网站支持，已添加到订阅"
                context.bot.send_message(chat_id=chat.id, text=text)
            else:
                text = "该网站尚未支持"
                context.bot.send_message(chat_id=chat.id, text=text)

# 小组
def join_group(update: Update, context: CallbackContext):
    """加入小组"""
    global group_name
    chat = update.effective_chat
    if context.args:
        group_name = context.args[0]
    logger.info(f"{chat.username}加入{group_name}")
    

def create_group(update: Update, context: CallbackContext):
    """创建小组"""
    global group_name
    chat = update.effective_chat
    if context.args:
        group_name = context.args[0]
    logger.info(f"{chat.username}加入{group_name}")

def del_group(update: Update, context: CallbackContext):
    """删除小组"""
    global group_name
    chat = update.effective_chat
    if context.args:
        group_name = context.args[0]
    logger.info(f"{chat.username}加入{group_name}")
    

def exit_group(update: Update, context: CallbackContext):
    """退出小组"""
    global group_name
    if context.args:
        group_name = context.args[0]
    logger.info(group_name)

# 其他
def change_time(update: Update, context: CallbackContext):
    """梗概时区"""
    
def cancel(update: Update, context: CallbackContext):
    """取消会话"""
    return ConversationHandler.END

def help(update: Update, context: CallbackContext):
    """显示帮助"""
    chat = update.effective_chat
#     text = """帮助
# 可用命令
# - /start ——> 开始使用
# - /register ——> 注册
# - /list ——> 订阅列表
# - /time ——> 时区
# - /create_group + <组名>——> 创建小组
# - /del_group + <组名> ——> 删除小组
# - /del + <订阅链接/序号> ——> 删除链接
# - /join_group + <组名> ——> 加入小组
# - / ——>
# - / ——>
# - / ——>
# """
    text = """帮助
/register ——> 注册
/list ——> 订阅列表
(目前仅支持kktv,friday)"""
    context.bot.send_message(chat_id=chat.id, text=text)
    
def extract_status_change(
    chat_member_update: ChatMemberUpdated,
) -> Optional[Tuple[bool, bool]]:
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    获取 ChatMemberUpdated 实例并提取“old_chat_member”是否是成员 聊天以及“new_chat_member”是否是聊天的成员。返回无，如果 状态没有改变。
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = (
        old_status
        in [
            ChatMember.MEMBER,
            ChatMember.CREATOR,
            ChatMember.ADMINISTRATOR,
        ]
        or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    )
    is_member = (
        new_status
        in [
            ChatMember.MEMBER,
            ChatMember.CREATOR,
            ChatMember.ADMINISTRATOR,
        ]
        or (new_status == ChatMember.RESTRICTED and new_is_member is True)
    )

    return was_member, is_member

def greet_chat_members(update: Update, context: CallbackContext) -> None:
    """在聊天中问候新用户并在有人离开时通知"""
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()

    if not was_member and is_member:
        update.effective_chat.send_message(
            f"{member_name} 加入了 {cause_name}. Welcome!",
            parse_mode=ParseMode.HTML,
        )
    elif was_member and not is_member:
        update.effective_chat.send_message(
            f"{member_name}离开了聊天室. Thanks a lot, {cause_name} ...",
            parse_mode=ParseMode.HTML,
        )
    
def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'处理更新时引发异常\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    # Finally, send the message
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)


def bad_command(update: Update, context: CallbackContext) -> None:
    """Raise an error to trigger the error handler."""
    context.bot.wrong_method_name()  # type: ignore[attr-defined]

def main() -> None:
    """运行bot"""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1784957255:AAFiO1Id7l3OERSlhywpjXq71_MCITSxxS8")
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # Register the commands...
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~(
                Filters.command | Filters.regex('^Cancel$')),
            check_link))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("join_group", join_group))
    dispatcher.add_handler(CommandHandler("create_group", create_group))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler('bad_command', bad_command))

    # ...and the error handler
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()