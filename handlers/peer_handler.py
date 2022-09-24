import json
import logging

from pathlib import Path

from aiocache import cached
from aiopathlib import AsyncPath

from vkbottle import VKAPIError
from vkbottle import API

from settings import peer_default_dict
from config.bot_cfg import BOT_TOKEN


class PeerHandler():
    def __init__(self):
        self.peers_folder = Path("peers")
        self.peers_folder.mkdir(exist_ok=True)
        self.peer_json_name = "main.json"
        
        self.peer_settings = {}
        self.peers_messages = {}
        
        self.admins = self.Admins(self)
        self.settings = self.Settings(self)
        self.messages = self.Messages(self)

        logging.info("LOADING PEERS SETTINGS")
        for peer_object in self.peers_folder.rglob("main.json"):
            peer_id = int(peer_object.parent.stem)
            with peer_object.open("r", encoding="utf-8") as peer_info:
                if peer_object.stem == "main":
                    self.peer_settings[peer_id] = json.load(peer_info)
        logging.info(f"PEERS SETTINGS LOADED ({len(self.peer_settings)} units)")

        
    async def save(self, peer_id: int):
        fp = AsyncPath(self.peers_folder, str(peer_id), self.peer_json_name)
        await fp.write_json(self.peer_settings[peer_id], indent=4, encoding="utf8", ensure_ascii=False)
        logging.info(f"PEER ({peer_id}) SETTINGS SAVED")


    async def create_peer_unit(self, peer_id: int):
        self.peer_settings[peer_id] = peer_default_dict
        await self.save(peer_id)
        logging.warning(f"{peer_id} - Default settings added for new peer")


    async def get(self, peer_id: int, key: str):
        await self._check_peer_exist(peer_id)
        return self.peer_settings[peer_id][key]


    async def add(self, peer_id: int, peer_key: str, value: dict):
        await self._check_peer_exist(peer_id)
        self.peer_settings[peer_id][peer_key].update(value)


    def _edit_dict(self, peer_id: int, key: any, value: any):
        self.peer_settings[peer_id][key] = value

    
    async def _check_peer_exist(self, peer_id: int):
        peer_folder = AsyncPath(self.peers_folder, str(peer_id))
        if not await peer_folder.is_dir():
            await peer_folder.mkdir()
            await self.create_peer_unit(peer_id)


    class Messages():
        def __init__(self, parent):
            self.peerhandler = parent
            self.message_filename = "messages.json"


        @cached(ttl=120)
        async def _get_peer_messages(self, peer_id: str, user_id: str = None) -> dict:
            await self.peerhandler._check_peer_exist(int(peer_id))
            messages = {}
            for peer_object in AsyncPath(self.peerhandler.peers_folder).rglob("messages.json"):
                peer_id_folder = peer_object.parent.stem
                if peer_id == peer_id_folder:
                    messages[peer_id] = await AsyncPath(peer_object).read_json(encoding="utf8")
            if peer_id not in messages.keys():
                messages.setdefault(peer_id, {})
                messages[peer_id]["messages_count"] = 0
            if user_id is not None:
                if user_id not in messages[peer_id]:
                    messages[peer_id].setdefault(user_id, {})
                    messages[peer_id][user_id]["messages_count"] = 0
                    messages[peer_id][user_id].setdefault("messages", [])
            return messages

 
        async def write(self, message_text: str, cmid: int, peer_id: str, user_id: str, date: float):
            messages = await self._get_peer_messages(peer_id, user_id)
            messages[peer_id][user_id]["messages"].append({
                "message_text": message_text,
                "cmid": cmid,
                "date": date
            })
            messages[peer_id]["messages_count"] += 1
            messages[peer_id][user_id]["messages_count"] += 1
            fp = AsyncPath(self.peerhandler.peers_folder, peer_id, self.message_filename)
            await fp.write_json(messages[peer_id], indent=4, encoding="utf8", ensure_ascii=False)
            

    class Settings():
        def __init__(self, parent):
            self.peerhandler = parent
        
        async def set_greeting(self, peer_id: int, text: str):
            await self.peerhandler._check_peer_exist(peer_id)
            self.peerhandler._edit_dict(peer_id, "greeting", text)
            await self.peerhandler.save(peer_id)
        
        async def set_rules(self, peer_id: int, text: str):
            await self.peerhandler._check_peer_exist(peer_id)
            self.peerhandler._edit_dict(peer_id, "rules", text)
            await self.peerhandler.save(peer_id)


    class Admins():
        def __init__(self, parent):
            self.peerhandler = parent
            self.api = API(token=BOT_TOKEN)


        async def get_list(self, peer_id: int) -> list:
            await self.peerhandler._check_peer_exist(peer_id)
            if not self.peerhandler.peer_settings[peer_id]["admins"]:
                await self.renew(peer_id)
            return self.peerhandler.peer_settings[peer_id]["admins"]


        def add(self, peer_id: int, user_id: int):
            self.peerhandler.add(peer_id, "admins", user_id)


        async def renew(self, peer_id: int):
            try:
                members = await self.api.request("messages.getConversationMembers", {"peer_id":peer_id})
            except VKAPIError[917]:
                return
            
            peer_admins = [int(member['member_id']) for member in members['response']['items'] if 'is_admin' in member]
            self.peerhandler._edit_dict(peer_id, "admins", peer_admins)