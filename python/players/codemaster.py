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
        clue = clue_input.split(" ")

        if len(clue) == 1:
            clue.append('1')

        return clue


class bot_codemaster(codemaster):

    def __init__(self):
        pass


    def get_board(self,words):
        self.words = words


    def get_bot_text(self, bot_array):
        self.bot_array = bot_array


    def give_clue(self):

        # assuming none of the words in botwordlist is also in CNwordlist, gotta add that
        f = open("BotWordList.txt", "r")
        if f.mode == 'r':
            temp_arr = f.read().splitlines()

        bot_string_input = random.choice(temp_arr)
        bot_num_input = random.randint(1, 8)
        clue = [str(bot_string_input), str(bot_num_input)]
        return clue



