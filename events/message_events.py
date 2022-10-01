import methods

from types import ModuleType
from vkbottle.bot import Message
from vkbottle_types.objects import MessagesMessageActionStatus
from settings import bot_commands
from rules import IsAdmin, NoCaseRegexRule
from loader import bot, logger
from methods import decorators
from datatypes import PeerObject, user

bot.labeler.custom_rules["is_admin"] = IsAdmin
bot.labeler.custom_rules["regex"] = NoCaseRegexRule

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
    group_id = event.group_id
    peer_id = event.peer_id
    member_id = action.member_id
    if action.type != MessagesMessageActionStatus.CHAT_KICK_USER:
        if not action or not group_id:
            return
        if member_id == -group_id:
            logger.info("BOT INVITED",id=peer_id)
            await event.answer(f"""
                👋Всем привет! Я - Ричи, чатбот созданный для удобного администрирования бесед ВКонтакте! 
                (не забудьте назначить бота администратором беседы, иначе он не работает)
                Список команд - https://vk.com/@richie_bot-richi-komandy-ver3
                Или используйте "ричи команды"
            """)
        else:
            if (greeting := peer_obj.data.greeting):
                await event.answer(greeting)


@bot.on.chat_message(regex=non_adm_commands)
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
            def_function_name, peer_obj, event.from_id
        )
        if command_args[0] is None: return
        if onreply := event.reply_message:
            command_args[0] = await user.get_user(onreply.from_id, event.peer_id)
        else: 
            if command_args[0] is None: return
        def_func = bot_commands.default_commands_notfull[command_name]
    if isinstance(def_func, ModuleType):
        await event.answer("Команда есть. Не реализована.")
    else:
        await def_func(event, peer_obj, command_args)


@bot.on.chat_message(regex=adm_commands, is_admin=True)
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
            adm_function_name, peer_obj, event.from_id
        )
        if onreply := event.reply_message:
            command_args[0] = await user.get_user(onreply.from_id, event.peer_id)
        else:
            if command_args[0] is None: return
            
        adm_func = bot_commands.administrative_commands_notfull[command_name]

    if isinstance(adm_func, ModuleType):
        await event.answer("Команда есть. Не реализована.")
    else:
        await adm_func(event, peer_obj, command_args)


@bot.on.chat_message()
@decorators.peer_manager
async def log_message(event: Message, peer_obj: PeerObject) -> None:
    await peer_obj.messages.write(
        message_text = event.text, 
        cmid = event.message_id,
        user_id = str(event.from_id),
        date = event.date,
        user = await user.get_user(event.from_id, event.peer_id)
    )