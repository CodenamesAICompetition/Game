import random
import array
import os
import sys

from players.codemaster import *
from players.guesser import *
# should install Wordnet through nltk and also textblob
from textblob import Word

# https://codeshare.io/aJgPVZ
# if default python version isn't python3, must use python3 when running on terminal

class Game:

    guesser = 0
    words = 0
    codemaster = 0
    map = 0 


    def __init__(self):
        
        if sys.argv[1] == "human":
            self.codemaster = human_codemaster()
        else:
            self.codemaster = bot_codemaster()

        if sys.argv[2] == "human":
            self.guesser = human_guesser()
        else:
            self.guesser = bot_guesser()

        # open the text file for random selection - readonly
        f = open("CNWordList.txt", "r")
        # if successfully opened split and randomly generate 25 words
        if f.mode == 'r':            
            # contains all words from text file as an array
            temp_array = f.read().splitlines()
            self.words = set([])
            # initialize the set words randomly
            for x in range(0, 25):
                self.words.add(random.choice(temp_array))

            # if duplicates were detected and the set length is not 25 then restart
            if len(self.words) != 25:
                self.__init__()

            # initialize back as a list
            self.words = list(self.words)

        self.map = ["Red"]*8 + ["Blue"]*7 + ["Civilian"]*9 + ["Assassin"]
        random.shuffle(self.map)



    def display_board(self):

        print(str.center("___________________________BOARD___________________________", 60))

        for i in range(len(self.words)):
            # newline for every 5 prints
            if i % 5 == 0:
                print("\n")
            # centers the output
            print(str.center(self.words[i], 10), " ", end='')

        print(str.center("\n___________________________________________________________", 60))

        print("\n")


    def display_map(self):

        print("\n")
        print(str.center("____________________________MAP____________________________", 55))

        for i in range(len(self.map)):
            # newline for every 5 prints
            if i % 5 == 0:
                print("\n")
            # centers the output
            print(str.center(self.map[i], 10), " ", end='')

        print(str.center("\n___________________________________________________________", 55))

        print("\n")


    def list_words(self):

        return self.words


    # takes in an int index called guess to compare with the Map
    def accept_guess(self,guess_index):

        # CodeMaster will always win with Red and lose with Blue or Assassin
        if self.map[guess_index] == "Red":

            if self.words.count("*Red*") >= 8:

                return "Win"

            self.words[guess_index] = "*Red*"
            return "Hit_Red"

            
        elif self.map[guess_index] == "Blue":

            self.words[guess_index] = "*Blue*"

            if self.words.count("*Blue*") >= 7:

                return "Lose"
                
            else:

                return "Still Going"

        elif self.map[guess_index] == "Assassin":

            self.words[guess_index] = "*Assassin*"
            return "Lose"

        else:
            self.words[guess_index] = "*Civilian*"
            return "Still Going"

          
    def cls(self):
      
        print('\n'*11)
        
        
    def run(self):
      
        string_win_condition = "Hit_Red"
        print("========================GAME START========================\n")

      
        while(string_win_condition != "Lose" or string_win_condition != "Win"):
          
            self.cls()
            words_in_play = self.list_words()
            self.codemaster.get_board(words_in_play)
            
            self.display_board()
            self.display_map()
            
            clue, num = self.codemaster.give_clue()
            num = int(num)
            number = num
            clue = str(clue)
            
            self.cls()
            self.display_board()
            self.guesser.get_clue(clue,num)
            
            string_win_condition = "Hit_Red"
            
            while(string_win_condition == "Hit_Red" and num >= 0):

                num -= 1
                self.guesser.get_board(words_in_play)

                guess_answer = self.guesser.give_answer()

                guess_answer_index = words_in_play.index(guess_answer.upper())

                string_win_condition = self.accept_guess(guess_answer_index)


                if string_win_condition == "Hit_Red":
                    
                    self.cls()
                    self.display_board()
                    print("The clue is : ",clue," ",number,sep="")
                    
                elif string_win_condition == "Still Going":
                    break

                elif string_win_condition == "Lose":
                    self.display_board()
                    print("You Lost")
                    exit()
                    

                elif string_win_condition == "Win":
                    self.display_board()
                    print("You Won")
                    exit()


if __name__ == "__main__":
    game = Game()
    game.run()


