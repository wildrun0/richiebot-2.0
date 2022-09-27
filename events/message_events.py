import logging
import methods

from types import ModuleType
from vkbottle.bot import Message

from settings import bot_commands
from rules import IsAdmin
from loader import bot
from methods import decorators
from datatypes.user import get_user
from datatypes import PeerObject


bot.labeler.custom_rules["is_admin"] = IsAdmin

FULL_COMMAND_REGEX = "^%s$"
non_adm_commands = (
    *(FULL_COMMAND_REGEX % i for i in bot_commands.all_commands_full), 
    *bot_commands.all_commands_notfull
)
adm_commands = (
    *(FULL_COMMAND_REGEX % i for i in bot_commands.admin_commands_full),
    *bot_commands.admin_commands_notfull
)
logging.debug(f"Regex ({FULL_COMMAND_REGEX}) set for 'full' commands")

@bot.on.chat_message(action=["chat_invite_user", "chat_kick_user"])
@decorators.peer_manager
async def invite_event(event: Message, peer_obj: PeerObject) -> None:
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
        if (greeting := peer_obj.data.greeting):
            await event.answer(greeting)
        await peer_obj.save()


@bot.on.chat_message(regexp=non_adm_commands)
@decorators.peer_manager
async def use_default_commands(event: Message, peer_obj: PeerObject) -> None:
    def_function_name = event.text.lower()
    try:
        def_func = bot_commands.default_commands_full[def_function_name]
        command_name = def_function_name
        command_args = None
    except KeyError:
        command_name, command_args = await methods.get_command_arguments(
            bot_commands.all_commands_notfull, 
            def_function_name, peer_obj
        )

        if command_args and not command_args[0]:
            if onreply := event.reply_message:
                command_args = await get_user(onreply.from_id), command_args[2:]
            else: return

        def_func = bot_commands.default_commands_notfull[command_name]

    if isinstance(def_func, ModuleType):
        await event.answer("Команда есть. Не реализована.")
    else:
        event.text = event.text.replace(command_name, "").lstrip()
        await def_func(event, peer_obj, command_args)


@bot.on.chat_message(regexp=adm_commands, is_admin=True)
@decorators.peer_manager
async def use_admin_commands(event: Message, peer_obj: PeerObject) -> None:
    adm_function_name = event.text.lower()
    try:
        adm_func = bot_commands.administrative_commands_full[adm_function_name]
        command_name = adm_function_name
        command_args = None
    except KeyError:
        command_name, command_args = await methods.get_command_arguments(
            bot_commands.admin_commands_notfull, 
            adm_function_name, peer_obj
        )

        if command_args and not command_args[0]:
            if onreply := event.reply_message:
                command_args = await get_user(onreply.from_id), command_args[2:]
            else: return

        adm_func = bot_commands.administrative_commands_notfull[command_name]

    if isinstance(adm_func, ModuleType):
        await event.answer("Команда есть. Не реализована.")
    else:
        event.text = event.text.replace(command_name, "").lstrip()
        await adm_func(event, peer_obj, command_args)


@bot.on.chat_message()
@decorators.peer_manager
async def log_message(event: Message, peer_obj: PeerObject) -> None:
    await peer_obj.messages.write(
        message_text = event.text, 
        cmid = event.message_id,
        user_id = str(event.from_id),
        date = event.date
    )