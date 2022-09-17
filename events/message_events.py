import logging
from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import ChatActionRule
from rules import AdminCommandUse, CommandUse, IsAdmin
from loader import bot, peers_handler
from utilities import Utils as utils
from settings import bot_commands


@bot.on.chat_message(ChatActionRule("chat_invite_user"))
async def bot_invite(event: Message) -> None:
    action = event.action
    group_id = event.group_id
    if not action or not group_id:
        return
    if action.member_id == -group_id:
        await event.answer(f"""
            👋Всем привет! Я - ричи, чатбот созданный для удобного администрирования бесед ВКонтакте! 
            (не забудьте назначить бота администратором беседы, иначе он не работает)
            Список команд - https://vk.com/@richie_bot-richi-komandy-ver3
            Или используйте "ричи команды"
        """)
        logging.info(f"Bot invited in {event.peer_id}")
        peers_handler.save(event.peer_id)


@bot.on.chat_message(CommandUse())
async def use_default_commands(event: Message) -> None:
    def_function_name = event.text.lower()
    if command_name := utils.command_used(
        bot_commands.all_commands_full, 
        def_function_name,
        return_command_name=True
    ):
        def_func = bot_commands.default_commands_full[command_name]
    elif command_name := utils.command_used(
        bot_commands.all_commands_notfull, 
        def_function_name,
        return_command_name=True
    ):
        def_func = bot_commands.default_commands_notfull[command_name]

    await def_func(event)


@bot.on.chat_message(AdminCommandUse(), IsAdmin())
async def use_admin_commands(event: Message) -> None:
    adm_function_name = event.text.lower()
    if command_name := utils.command_used(
        bot_commands.admin_commands_full, 
        adm_function_name,
        return_command_name=True
    ):
        adm_func = bot_commands.administrative_commands_full[command_name]
    elif command_name := utils.command_used(
        bot_commands.admin_commands_notfull, 
        adm_function_name,
        return_command_name=True
    ):
        adm_func = bot_commands.administrative_commands_notfull[command_name]

    await adm_func(event)