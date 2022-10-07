import textwrap
import zlib

from datatypes import PeerObject
from datatypes.user import get_user
from vkbottle.bot import Message
from vkbottle_types.codegen.objects import MessagesConversation


def word_count(message):
    counts = {}
    words = message.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

async def stats(event: Message, peer_obj: PeerObject, param: None):
    peer_id = event.peer_id

    chat_info: MessagesConversation = (
        await event.ctx_api.messages.get_conversations_by_id(
            peer_ids = peer_id
        )
    ).items[0]
    
    chat_title = chat_info.chat_settings.title
    chat_members = len(peer_obj.data.users)
    chat_owner = (await get_user(peer_obj.data.owner_id, peer_id)).get_nickname(peer_id)
    chat_total_messages = event.conversation_message_id
    
    chat_recent_activity_ids = chat_info.chat_settings.active_ids
    chat_recent_activity = [
        (await get_user(uid, peer_id)).get_nickname(peer_id) 
        for uid in chat_recent_activity_ids
    ]
    
    chat_total_banned = len(peer_obj.data.ban_list)
    chat_total_muted = len(peer_obj.data.mute)
    
    words = {}
    for profile in peer_obj.messages.data.users.values():
        total_usrs_msgs = " ".join(
            zlib.decompress(msg.message_text).decode("utf8") for msg in profile.messages
        )
        words.update(word_count(total_usrs_msgs))

    most_used_words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))
    top5_used_words = list(most_used_words.items())[:5]

    to_send = textwrap.dedent("""
    Беседа '%s'
    👑Создатель: %s
    👥Всего пользователей: %d
    💬Всего сообщений: %s
    🚫Пользователей забанено: %d
    🔇Пользователей в муте: %d
    🔝Топ 5 использованых слов за эту неделю:
    """)

    for enum, (word, times) in enumerate(top5_used_words):
        to_send += f"{enum + 1}. ' {word} ': {times}\n"

    to_send += "Последние активные пользователи:\n"
    for index, usr in enumerate(chat_recent_activity):
        to_send += f"{index+1}. {usr}\n"
    
    await event.answer(
        to_send % (chat_title, chat_owner, chat_members, f"{chat_total_messages:,}", chat_total_banned, chat_total_muted),
    disable_mentions=True)
