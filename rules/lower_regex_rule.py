import re
from typing import Pattern
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule


class LowerCaseRegexRule(ABCRule[Message]):
    def __init__(self, regexp: str | list[str] | Pattern | list[Pattern]):
        if isinstance(regexp, Pattern):
            regexp = [regexp]
        elif isinstance(regexp, str):
            regexp = [re.compile(regexp)]
        elif isinstance(regexp, list):
            regexp = [re.compile(exp) for exp in regexp]

        self.regexp = regexp

    async def check(self, event: Message) -> dict[str, tuple] | bool:
        for regexp in self.regexp:
            match = re.match(regexp, event.text.lower())
            if match:
                return {"match": match.groups()}
        return False