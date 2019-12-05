import random


class codemaster():

    words = 0
    maps = 0
    bot_array = 0

    def __init__(self, brown_ic=None, glove_vecs=None, word_vectors=None):
        pass

    def receive_game_state(self, words_in_play, map_in_play):
        self.words = words_in_play
        self.maps = map_in_play

    def give_clue(self):
        pass


class human_codemaster(codemaster):

    def __init__(self, brown_ic=None, glove_vecs=None, word_vectors=None):
        pass

    def receive_game_state(self, words_in_play, map_in_play):
        self.words = words_in_play
        self.maps = map_in_play
        
    def give_clue(self):
        clue_input = input("Input CM Clue:\nPlease enter a Word followed by a space and a Number >> ")
        clue_input = clue_input.strip()
        type(clue_input)
        clue = clue_input.split(" ")

        if len(clue) == 1:
            clue.append('1')
        return clue
