#codemaster

from abc import ABC, abstractmethod
import random

class codemaster(ABC):

    words = 0
    map = 0
    bot_array = 0
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

    def __init__(self):
        pass


    def get_board(self,words):

        self.words = words

    def get_bot_text(self, bot_array):

        self.bot_array = bot_array

    def __init__(self):

        f = open("BotWordList.txt", "r")
        if f.mode == 'r':
            temp_arr = f.read().splitlines()
            bot_array = set([])

        for x in range(0, 8):
            bot_array.add(random.choice(temp_arr))

        if len(bot_array) != 8:
            self.__init__()

        self.bot_array = list(bot_array)

    def give_clue(self):

        bot_clue_input = random.choice(self.bot_array)
        bot_num_input = random.randint(1, 3)
        clue = [str(bot_clue_input), str(bot_num_input)]
        return clue



