

async def length(event, string: str, MAX_LENGTH: int) -> bool:
    if len(string) > MAX_LENGTH:
        await event.answer(f"🚫Недопустимая длина ({len(string)}>{MAX_LENGTH})")
        return False
    return True
