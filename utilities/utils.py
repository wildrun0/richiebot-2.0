from cProfile import label
import os
from typing import Union
import time


cached_commands = {}
class Utils():
    @staticmethod
    def dir_empty(dir_path: str) -> bool:
        return not next(os.scandir(dir_path), None)
    
    
    @staticmethod
    def command_used(lists: list, text: str, check_call = False) -> Union[bool, int]:
        if check_call:
            return any(map(lambda b: any(map(text.startswith, b)), lists))
        else:
            for i in enumerate(map(lambda b: map(text.startswith, b), lists)):
                commands_indexes = list(i[1])
                idx = i[0]
                if True in commands_indexes:
                    return lists[idx][commands_indexes.index(True)], idx
        return False