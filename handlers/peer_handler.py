import json
import logging
from pathlib import Path
from aiopathlib import AsyncPath
from settings import peer_default_dict
from vkbottle import VKAPIError
from vkbottle import API
from config.bot_cfg import BOT_TOKEN


class PeerHandler():
    def __init__(self):
        self.peers_folder = Path("peers")
        self.peers_folder.mkdir(exist_ok=True)
        self.peer_json_name = "main.json"
        self.peer_settings = {}
        self.admins = self.Admins(self)
        self.settings = self.Settings(self)

        logging.info("LOADING PEERS SETTINGS")
        for peer_object in self.peers_folder.rglob(self.peer_json_name):
            peer_id = int(peer_object.parent.stem)
            with peer_object.open("r", encoding="utf-8") as peer_info:
                self.peer_settings[peer_id] = json.load(peer_info)
        logging.info(f"PEERS SETTINGS LOADED ({len(self.peer_settings)} units)")

        
    async def save(self, peer_id: int):
        fp = AsyncPath(self.peers_folder, str(peer_id), self.peer_json_name)
        await fp.write_json(self.peer_settings[peer_id], indent=4, ensure_ascii=False)
        logging.info(f"PEER ({peer_id}) SETTINGS SAVED")


    def create_peer_unit(self, peer_id: int):
        self.peer_settings[peer_id] = peer_default_dict
        logging.info(f"Default settings added for new peer ({peer_id})")


    async def get(self, peer_id: int, key: str):
        await self._check_peer_exist(peer_id)
        return self.peer_settings[peer_id][key]


    def _edit_dict(self, peer_id: int, key: any, value: any):
        self.peer_settings[peer_id][key] = value

    
    async def _check_peer_exist(self, peer_id: int):
        peer_folder = AsyncPath(self.peers_folder, str(peer_id))
        if not await peer_folder.is_dir():
            await peer_folder.mkdir()
            self.create_peer_unit(peer_id)


    class Messages():
        def __init__(self, parent):
            self.peerhandler = parent
            self.message_filename = "messages.json"


        # def write(self, message, message_id, user_id, timestamp):
            

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
            self.peerhandler._edit_dict(peer_id, "admins",
                [*self.peerhandler.peer_settings[peer_id]["admins"], user_id]
            )


        async def renew(self, peer_id: int):
            try:
                members = await self.api.request("messages.getConversationMembers", {"peer_id":peer_id})
            except VKAPIError[917]:
                return
            
            peer_admins = [int(member['member_id']) for member in members['response']['items'] if 'is_admin' in member]
            self.peerhandler._edit_dict(peer_id, "admins", peer_admins)