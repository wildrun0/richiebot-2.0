import logging
import utils
from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import ChatActionRule
from rules import AdminCommandUse, CommandUse, IsAdmin
from loader import bot, peers_handler
from settings import bot_commands

from types import ModuleType


@bot.on.chat_message(ChatActionRule("chat_invite_user"))
async def bot_invite(event: Message) -> None:
    action = event.action
    group_id = event.group_id
    if not action or not group_id:
        return
    if action.member_id == -group_id:
        logging.info(f"Bot invited in {event.peer_id}")
        peers_handler.save(event.peer_id)
        await event.answer(f"""
            👋Всем привет! Я - ричи, чатбот созданный для удобного администрирования бесед ВКонтакте! 
            (не забудьте назначить бота администратором беседы, иначе он не работает)
            Список команд - https://vk.com/@richie_bot-richi-komandy-ver3
            Или используйте "ричи команды"
        """)


@bot.on.chat_message(CommandUse())
async def use_default_commands(event: Message) -> None:
    def_function_name = event.text.lower()
    command_name, command_type = await utils.command_used((
        bot_commands.all_commands_notfull, # command_type 0
        bot_commands.all_commands_full     # command_type 1
    ), def_function_name)

    match command_type:
        case 0:
            def_func = bot_commands.default_commands_notfull[command_name]
        case 1:
            def_func = bot_commands.default_commands_full[command_name]

    if isinstance(def_func, ModuleType):
        await event.answer("Команда есть. Не реализована.")
    else:
        event.text = event.text.replace(command_name, "").lstrip()
        await def_func(event)


@bot.on.chat_message(AdminCommandUse(), IsAdmin())
async def use_admin_commands(event: Message) -> None:
    adm_function_name = event.text.lower()
    command_name, command_type = await utils.command_used((
        bot_commands.admin_commands_notfull,
        bot_commands.admin_commands_full
    ), adm_function_name)

    match command_type:
        case 0:
            adm_func = bot_commands.administrative_commands_notfull[command_name]
        case 1:
            adm_func = bot_commands.administrative_commands_full[command_name]

    if isinstance(adm_func, ModuleType):
        await event.answer("Команда есть. Не реализована.")
    else:
        event.text = event.text.replace(command_name, "").lstrip()
        await adm_func(event)