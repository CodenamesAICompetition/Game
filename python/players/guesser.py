#guesser.py

from abc import ABC, abstractmethod
import random
import players.wn_guesser as wn_guesser


class guesser(ABC):
    words = 0
    clue = 0

class human_guesser(guesser):


    def init(self):
        pass


    def get_clue(self, clue, num):
        print("The clue is:", clue, num, sep=" ")


    def get_board(self, words):
        self.words = words


    def give_answer(self):

        answer_input = input("Guesser makes turn.\nPlease enter a valid Word >> ")
        type(answer_input)

        while not self.is_valid(answer_input):

            print("Input Invalid")
            print(self.words)
            answer_input = input("Please enter a valid Word >> ")
            type(answer_input)

        return answer_input


    def is_valid(self, result):

        if result.upper() in self.words:
            return True

        else:
            return False


class bot_guesser(guesser):

    def get_board(self, words):

        self.words = words
        return words


    def get_clue(self, clue, num):

        self.clue = clue
        print("The clue is:", clue, num, sep=" ")

        li = [clue, num]
        return li


    def give_answer(self):

        sorted_results = wn_guesser.word_synset(self.clue, self.words)

        first_index_row = [i[0] for i in sorted_results]

        for i in first_index_row:
            print(i)

        # testing res, change here for voting alg when possible
        closest_synset = sorted_results[2][0]
        print(closest_synset)

        answer_input = closest_synset[5]
        print(answer_input)
        answer_input = str(answer_input)

        return answer_input


