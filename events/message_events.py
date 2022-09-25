import logging
import utils

from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import ChatActionRule
from vkbottle import VKAPIError

from rules import AdminCommandUse, CommandUse, IsAdmin

from loader import bot
from methods import peer_object
from datatypes.user.get_user import get_user
from handlers.peer_handler import PeerObject
from settings import bot_commands

from types import ModuleType


@bot.on.chat_message(ChatActionRule("chat_invite_user"))
@peer_object
async def bot_invite(event: Message, peer_obj: PeerObject) -> None:
    action = event.action
    group_id = event.group_id
    peer_id = event.peer_id
    if not action or not group_id:
        return
    if (member_id := action.member_id) == -group_id:
        logging.info(f"Bot invited in {peer_id}")
        await event.answer(f"""
            👋Всем привет! Я - ричи, чатбот созданный для удобного администрирования бесед ВКонтакте! 
            (не забудьте назначить бота администратором беседы, иначе он не работает)
            Список команд - https://vk.com/@richie_bot-richi-komandy-ver3
            Или используйте "ричи команды"
        """)
    else:
        peer_obj.data.users.append(member_id)
        if str(member_id) in peer_obj.data.ban_list:
            try:
                await event.ctx_api.messages.remove_chat_user(event.chat_id, member_id = member_id)
                peer_obj.data.users.remove(member_id)
                await event.answer("Пользователь находится в бане")
            except VKAPIError[925]: pass
        else:
            if (greeting := peer_obj.data.greeting):
                await event.answer(greeting)


@bot.on.chat_message(CommandUse())
@peer_object
async def use_default_commands(event: Message, peer_obj: PeerObject) -> None:
    def_function_name = event.text.lower()
    command_name, command_args, command_type = await utils.command_used((
        bot_commands.all_commands_notfull, # command_type 0
        bot_commands.all_commands_full     # command_type 1
    ), def_function_name)

    if command_args and not command_args[0]:
        if onreply := event.reply_message:
            command_args = await get_user(onreply.from_id), command_args[2:]
        else: return

    match command_type:
        case 0:
            def_func = bot_commands.default_commands_notfull[command_name]
        case 1:
            def_func = bot_commands.default_commands_full[command_name]

    if isinstance(def_func, ModuleType):
        await event.answer("Команда есть. Не реализована.")
    else:
        event.text = event.text.replace(command_name, "").lstrip()
        await def_func(event, peer_obj, command_args)


@bot.on.chat_message(AdminCommandUse(), IsAdmin())
@peer_object
async def use_admin_commands(event: Message, peer_obj: PeerObject) -> None:
    adm_function_name = event.text.lower()
    command_name, command_args, command_type = await utils.command_used((
        bot_commands.admin_commands_notfull,
        bot_commands.admin_commands_full
    ), adm_function_name)

    if command_args and not command_args[0]:
        if onreply := event.reply_message:
            command_args = await get_user(onreply.from_id), command_args[2:]
        else: return

    match command_type:
        case 0:
            adm_func = bot_commands.administrative_commands_notfull[command_name]
        case 1:
            adm_func = bot_commands.administrative_commands_full[command_name]

    if isinstance(adm_func, ModuleType):
        await event.answer("Команда есть. Не реализована.")
    else:
        event.text = event.text.replace(command_name, "").lstrip()
        await adm_func(event, peer_obj, command_args)


@bot.on.chat_message()
@peer_object
async def log_message(event: Message, peer_obj: PeerObject) -> None:
    await peer_obj.messages.write(
        message_text = event.text, 
        cmid = event.message_id,
        user_id = str(event.from_id),
        date = event.date
    )