import textwrap
from types import ModuleType
from vkbottle_types.objects import MessagesMessageActionStatus
from vkbottle.bot import Message

import commands
import methods
from datatypes import PeerObject, user
from loader import bot, logger
from methods import decorators
from settings import bot_commands

FULL_COMMAND_REGEX = "^%s$"
non_adm_commands = (
    *(FULL_COMMAND_REGEX % i for i in bot_commands.all_commands_full), 
    *bot_commands.all_commands_notfull
)
adm_commands = (
    *(FULL_COMMAND_REGEX % i for i in bot_commands.admin_commands_full),
    *bot_commands.admin_commands_notfull
)
logger.debug(f"Regex ({FULL_COMMAND_REGEX}) set for 'full' commands")

@bot.on.chat_message(action=["chat_invite_user", "chat_kick_user"])
@decorators.peer_manager
async def invite_event(event: Message, peer_obj: PeerObject) -> None:
    action = event.action
    if action.type != MessagesMessageActionStatus.CHAT_KICK_USER:
        group_id = event.group_id
        if not action or not group_id:
            return
        if action.member_id == -group_id:
            logger.info("BOT INVITED",id=event.peer_id)
            await event.answer(textwrap.dedent("""
            👋Всем привет! Я - Ричи, чатбот созданный для удобного администрирования бесед ВКонтакте! 
            (не забудьте назначить бота администратором беседы, иначе он не работает)
            Список команд - https://vk.com/@richie_bot-richi-komandy-ver3
            Или используйте "ричи команды"
            """))
        else:
            if greeting := peer_obj.data.greeting:
                await event.answer(greeting)


@bot.on.chat_message(regex=non_adm_commands)
@decorators.peer_manager
async def use_default_commands(event: Message, peer_obj: PeerObject) -> None:
    try:
        def_function_name = event.text.lower()
        def_func = bot_commands.default_commands_full[def_function_name]
        command_name = def_function_name
        command_args = None
    except KeyError:
        command_name, command_args = await methods.get_command_arguments(
            bot_commands.all_commands_notfull, 
            event.text, peer_obj
        )
        if onreply := event.reply_message:
            index = 0
            for enum, i in enumerate(command_args):
                if i is None:
                    index = enum
            command_args[index] = await user.get_user(onreply.from_id, event.peer_id)
        else: 
            if None in command_args: return
        def_func = bot_commands.default_commands_notfull[command_name]
    if isinstance(def_func, ModuleType):
        await event.answer("Команда есть. Не реализована.")
    else:
        await def_func(event, peer_obj, command_args)


@bot.on.chat_message(regex=adm_commands, is_admin=True)
@decorators.peer_manager
async def use_admin_commands(event: Message, peer_obj: PeerObject) -> None:
    try:
        adm_function_name = event.text.lower()
        adm_func = bot_commands.administrative_commands_full[adm_function_name]
        command_name = adm_function_name
        command_args = None
    except KeyError:
        command_name, command_args = await methods.get_command_arguments(
            bot_commands.admin_commands_notfull, 
            event.text, peer_obj
        )
        adm_func = bot_commands.administrative_commands_notfull[command_name]
        if onreply := event.reply_message:
            index = 0
            for enum, i in enumerate(command_args):
                if i is None:
                    index = enum
            command_args[index] = await user.get_user(onreply.from_id, event.peer_id)
        else:
            if (None in command_args) and (
            # Нужно получать сырые id т.к. их нет в беседе
            (not (adm_func is commands.admin.unban)) and
            (not (adm_func is commands.admin.kick))): return
    if isinstance(adm_func, ModuleType):
        await event.answer("Команда есть. Не реализована.")
    else:
        await adm_func(event, peer_obj, command_args)


@bot.on.chat_message()
@decorators.peer_manager
async def log_message(event: Message, peer_obj: PeerObject) -> None:
    await peer_obj.messages.write(
        message_text = event.text, 
        user_id = str(event.from_id),
        cmid = event.message_id,
        date = event.date,
        user = await user.get_user(event.from_id, event.peer_id)
    )