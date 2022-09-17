import os
from typing import Union


class Utils():
    @staticmethod
    def dir_empty(dir_path: str) -> bool:
        return not next(os.scandir(dir_path), None)
    
    
    @staticmethod
    def command_used(commands_list: list, text: str, return_command_name: bool = False) -> Union[bool, str]:
        for command_elem in commands_list:
            command_string = command_elem.split(" ")

            total_matches = len(command_string)        
            string_matches = 0

            given_string_splited = text.split(" ")
            try:
                for i in range(len(given_string_splited)-1):
                    if given_string_splited[i] == command_string[i]:
                        string_matches += 1
            except IndexError: 
                continue

            if string_matches == total_matches:
                if return_command_name:
                    return command_elem
                else:
                    return True
        return False