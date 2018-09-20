from abc import ABC, abstractmethod

class codemaster(ABC):
    words = 0
    map = 0
    def __init__(self):
        pass
    def get_map(self,map_list):
        self.map = map_list
        
    def give_clue(self):
        pass

class human_codemaster(codemaster):
        def __init__(self):
                pass
        def get_board(self,words):
                self.words = words

        def give_clue(self):
                clue_input = input("Input CM Clue:\nPlease enter a Word followed by a space and a Number >> ")
                type(clue_input)
                clue = clue_input.split()
                return clue
                
class bot_codemaster(codemaster):
        def __init__():
            pass
