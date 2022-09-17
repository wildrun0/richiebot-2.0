from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule
from settings import bot_commands
from utilities import Utils as utils


class AdminCommandUse(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        command = event.text.lower()
        return (
            utils.command_used(bot_commands.admin_commands_notfull, command)
            or
            utils.command_used(bot_commands.admin_commands_full, command)
        )


class CommandUse(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        command = event.text.lower()
        return (
            utils.command_used(bot_commands.all_commands_full, command)
            or
            utils.command_used(bot_commands.all_commands_notfull, command)
        )