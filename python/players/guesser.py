#guesser.py

from abc import ABC, abstractmethod
import random

class guesser(ABC):
    words = 0

class human_guesser(guesser):

    def init(self):
        pass

    def get_clue(self,clue,num):

        print("The clue is: ",clue,num,sep="")


    def get_board(self,words):
        self.words = words



    def give_answer(self):

        # input answer
        answer_input = input("Guesser makes turn.\nPlease enter a valid Word >> ")
        type(answer_input)

        while not self.is_valid(answer_input):
            print("Input Invalid")
            print(self.words)
            answer_input = input("Please enter a valid Word >> ")
            type(answer_input)
        return answer_input


    def is_valid(self,result):

        if result.upper() in self.words:
            return True
        else:
            return False

class bot_guesser(guesser):

    def get_board(self, words):
        self.words = words

    def get_clue(self,clue,num):

        print("The clue is: ",clue,num,sep="")


    def give_answer(self):

        answer_input = "Hello"
        answer_input = random.choice(self.words)

        if(answer_input.startswith('*')):
            return self.give_answer()
        return answer_input

    #     while self.is_valid(answer_input):

            
    #         print("Input Invalid")
    #         print(self.words)

    #     return answer_input


    # def is_valid(self,result):

    #     if result.startswith('*'):
    #         return False
    #     else:
    #         return True

