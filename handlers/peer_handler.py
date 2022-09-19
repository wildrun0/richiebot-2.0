import json
import logging
from pathlib import Path
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


    def load(self, peer_id: int):
        peer_path = Path(self.peers_folder, str(peer_id))
        if not peer_path.is_dir():
            peer_path.mkdir()
        
        
    def save(self, peer_id: int):
        self._check_peer_exist(peer_id)

        with Path(self.peers_folder, str(peer_id), self.peer_json_name).open(mode="w", encoding="utf-8") as fp:
            json.dump(self.peer_settings[peer_id], fp, indent=4, ensure_ascii=False)
        logging.info(f"PEER ({peer_id}) SETTINGS SAVED")


    def create_peer_unit(self, peer_id: int):
        self.peer_settings[peer_id] = peer_default_dict
        logging.info(f"Default settings added for new peer ({peer_id})")


    def get(self, peer_id: int, key: str):
        return self.peer_settings[peer_id][key]


    def _edit_dict(self, peer_id: int, key: any, value: any):
        self.peer_settings[peer_id][key] = value

    
    def _check_peer_exist(self, peer_id: int):
        peer_folder = Path(self.peers_folder, str(peer_id))
        if not peer_folder.is_dir():
            peer_folder.mkdir()
            self.create_peer_unit(peer_id)


    class Settings():
        def __init__(self, parent):
            self.peerhandler = parent
        
        def set_greeting(self, peer_id: int, text: str):
            self.peerhandler._edit_dict(peer_id, "greeting", text)
            self.peerhandler.save(peer_id)
        
        def set_rules(self, peer_id: int, text: str):
            self.peerhandler._edit_dict(peer_id, "rules", text)
            self.peerhandler.save(peer_id)


    class Admins():
        def __init__(self, parent):
            self.peerhandler = parent
            self.api = API(token=BOT_TOKEN)


        async def get_list(self, peer_id: int) -> list:
            self.peerhandler._check_peer_exist(peer_id)
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