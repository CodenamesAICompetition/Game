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

        # answer input
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

        # answer inputesser makes turn.\nPlease enter a valid Word >> ")
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

    # def give_answer(self):

    #     # answer input
    #     temp_words = self.words.copy()

    #     # for every word in temp_words that starts with a * is removed from temp_words
    #     for word in temp_words:
    #         if word.startswith("*"):
    #             temp_words.remove(word)

    #     print("Guesser:\nPlease enter a valid Word >> ")
    #     bot_answer = random.choice(temp_words)
    #     temp_words.remove(bot_answer)
    #     print(bot_answer)

    #     return bot_answer

