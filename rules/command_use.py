import utils
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule
from settings import bot_commands


class AdminCommandUse(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        command = event.text.lower()
        return((await utils.command_used((
                bot_commands.admin_commands_notfull,
                bot_commands.admin_commands_full
            ), command, True))
        )


class CommandUse(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        command = event.text.lower()
        return(await utils.command_used((
                bot_commands.all_commands_notfull,
                bot_commands.all_commands_full,
            ), command, True)
        )